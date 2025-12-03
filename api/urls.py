from django.urls import path

from api import views

urlpatterns = [
    path("projects/", views.get_projects, name="get_projects"),
    path("projects/create/", views.create_project, name="create_project"),
]
