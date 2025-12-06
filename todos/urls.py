from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:id>', views.todos, name='todos'),
    path(
        'projects/<int:id>/delete/', views.delete_project, name='delete_project'
    ),
    path('projects/<int:id>/edit/', views.edit_project, name='edit_project'),
    path('projects/new', views.new_project, name='new_project'),
]
