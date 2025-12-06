from django.urls import path

from api import views

urlpatterns = [
    path('projects/', views.projects_list),
    path('projects/info', views.projects_info),
    path('projects/<int:pk>', views.project_detail),
    path('projects/create/', views.create_project),
]
