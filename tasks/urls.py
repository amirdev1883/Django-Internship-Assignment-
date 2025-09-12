from django.urls import path
from . import views
from . import api_views


app_name = 'tasks'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),

    path("create/", views.TaskCreateView.as_view(),  name='task_create'),
    path("update/<int:task_id>/", views.TaskUpdateView.as_view(),  name='task_update'),
    path("detail/<int:task_id>", views.TaskDetailView.as_view(),  name='task_detail'),
    path("list/", views.TaskListView.as_view(), name="task_list"),

    # API
    path('api/tasks/', api_views.TaskListCreateAPIView.as_view(), name='api_task_list_create'),
    path('api/tasks/<int:pk>/', api_views.TaskDetailAPIView.as_view(), name='api_task_detail'),
]

