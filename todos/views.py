from django.http import HttpResponse
from django.template import loader

from .models import Project, Todo


def projects(request):
    template = loader.get_template("projects.html")
    projects = Project.objects.all().values()
    context = {"projects": projects}
    return HttpResponse(template.render(context, request))


def todolist(request, id):
    template = loader.get_template("todos.html")
    project = Project.objects.get(id=id)
    todos = Todo.objects.filter(project=project)
    context = {
        "project": project,
        "todos": todos,
    }
    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))
