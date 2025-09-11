from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TaskUpdateCreateForm
from.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return redirect("tasks:home")  #change it later ----------------------------------------------- task list ----------
        # error message -----------------------------------------------------------
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
            return redirect("tasks:home") # change after to task detail 




    # def get(self, request, pk):
    #     task = get_object_or_404(Task, pk=pk, owner=request.user)
    #     form = self.form_class(instance=task)
    #     return render(request, "tasks/task_form.html", {"form": form, "update": True})

    # def post(self, request, pk):
    #     task = get_object_or_404(Task, pk=pk, owner=request.user)
    #     form = TaskUpdateCreateForm(request.POST, instance=task)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("tasks:task_list")
    #     return render(request, "tasks/task_form.html", {"form": form, "update": True})