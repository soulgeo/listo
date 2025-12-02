from django.urls import path

from api import views

urlpatterns = [path("projects/", views.get_projects, name="get_projects")]
