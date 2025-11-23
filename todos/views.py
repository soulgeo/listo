from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import ProjectDeleteForm, ProjectForm, TodoForm
from .models import Project, Todo


def projects(request):
    template = loader.get_template("projects.html")
    projects = Project.objects.all().values()
    context = {"projects": projects}
    return HttpResponse(template.render(context, request))


def todos(request, id):
    project = Project.objects.get(id=id)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if "add" in request.POST and form.is_valid():
            todo = Todo(name=form.cleaned_data["name"], project=project)
            todo.save()
        elif "update" in request.POST:
            todo_id = request.POST.get("update")
            todo = Todo.objects.get(id=todo_id)
            todo.is_complete = not todo.is_complete
            todo.save()
        elif "delete" in request.POST:
            todo_id = request.POST.get("delete")
            todo = Todo.objects.get(id=todo_id)
            todo.delete()

    template = loader.get_template("todos.html")
    form = TodoForm()
    todos = Todo.objects.filter(project=project)
    context = {
        "project": project,
        "todos": todos,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
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
