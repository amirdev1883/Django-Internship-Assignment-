from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TaskUpdateCreateForm
from.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator

class HomeView(View):
    def get(self, request):
        return render(request, 'tasks/index.html')


class TaskCreateView(LoginRequiredMixin, View):
    form_class = TaskUpdateCreateForm

    def get(self, request):
        form = self.form_class
        return render(request, "tasks/task_create_update.html", {"form": form, "update": False})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            messages.success(request, f'you created the task{new_task.title} successfully', 'success')
            return redirect("tasks:task_detail", task_id=new_task.id)  
        messages.error(request, 'form is not valid try again', 'danger')
        return render(request, "tasks/task_create_update.html", {"form": form})
    


class TaskUpdateView(LoginRequiredMixin, View):
    form_class = TaskUpdateCreateForm

    def setup(self, request, *args, **kwargs):
        self.task_inctanse = get_object_or_404(Task, pk=kwargs['task_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        task = self.task_inctanse
        if not request.user.id == task.owner.id:
            messages.error(request, 'you cant update this form ', 'danger')
            return redirect("tasks:home")
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        task = self.task_inctanse
        form = self.form_class(instance=task)
        return render(request, 'tasks/task_create_update.html', {'form': form, "update": True})

    def post(self, request, *args, **kwargs):
        task = self.task_inctanse
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'you updated the task successfully', 'success')
            return redirect("tasks:task_detail", task_id=task.id)  


class TaskDetailView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, owner=request.user)
        if task.owner != request.user:
            return HttpResponseForbidden("You are not allowed to view this task.")
        return render(request, "tasks/task_detail.html", {"task": task})
    

class TaskListView(LoginRequiredMixin, View):
    def get(self, request):
        # Base queryset: only the current user's tasks
        qs = Task.objects.filter(owner=request.user)

        # --- Filters / Search ---
        q = (request.GET.get("q") or "").strip()
        status = request.GET.get("status", "all")  # all | completed | pending
        date_from = request.GET.get("from") or ""
        date_to = request.GET.get("to") or ""
        sort = request.GET.get("sort", "due_date")  # due_date|due_date_desc|created|created_desc|title|title_desc

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if status == "completed":
            qs = qs.filter(completed=True)
        elif status == "pending":
            qs = qs.filter(completed=False)

        if date_from:
            qs = qs.filter(due_date__gte=date_from)
        if date_to:
            qs = qs.filter(due_date__lte=date_to)

        order_map = {
            "due_date": "due_date",
            "due_date_desc": "-due_date",
            "created": "created_at",
            "created_desc": "-created_at",
            "title": "title",
            "title_desc": "-title",
        }
        qs = qs.order_by(order_map.get(sort, "due_date"))

        # --- Pagination ---
        paginator = Paginator(qs, 10)  # 10 per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "q": q,
            "status": status,
            "date_from": date_from,
            "date_to": date_to,
            "sort": sort,
            "total_count": qs.count(),
        }
        return render(request, "tasks/task_list.html", context)