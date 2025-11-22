from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import ProjectDeleteForm, ProjectForm
from .models import Project, Todo


def projects(request):
    template = loader.get_template("projects.html")
    projects = Project.objects.all().values()
    context = {"projects": projects}
    return HttpResponse(template.render(context, request))


def todos(request, id):
    template = loader.get_template("todos.html")
    project = Project.objects.get(id=id)
    todos = Todo.objects.filter(project=project)
    context = {
        "project": project,
        "todos": todos,
    }
    return HttpResponse(template.render(context, request))


def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Process data
            project = Project(
                name=form.data["name"], description=form.data["description"]
            )
            project.save()
            return HttpResponseRedirect("/projects/")

    else:
        form = ProjectForm()

    template = loader.get_template("new_project.html")
    context = {
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def delete_project(request, id):
    project = Project.objects.get(id=id)
    if request.method == "POST":
        project.delete()
        return HttpResponseRedirect("/projects/")

    else:
        form = ProjectDeleteForm()

    template = loader.get_template("delete_project.html")
    context = {
        "form": form,
        "project": project,
    }
    return HttpResponse(template.render(context, request))


def home(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))
