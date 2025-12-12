from django.urls import path

from api import views

urlpatterns = [
    path('projects/', views.projects_list),
    path('projects/info/', views.projects_info),
    path('projects/<int:project_pk>/', views.project_detail),
    path('projects/create/', views.create_project),
    path('projects/update/<int:project_pk>/', views.update_project),
    path('projects/delete/<int:project_pk>/', views.delete_project),
    path('projects/<int:project_pk>/add/', views.add_todo),
    path('todo/<int:todo_pk>/', views.todo_detail),
    path('todo/<int:todo_pk>/complete/', views.complete_todo),
    path('todo/<int:todo_pk>/delete/', views.delete_todo),
]
