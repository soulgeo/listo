from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, render

from .forms import ProjectDeleteForm, ProjectForm, TodoForm
from .models import Project, Todo


def projects(request):
    projects = Project.objects.filter(user=request.user).values()
    context = {"projects": projects}
    return render(request, "projects.html", context)


def todos(request, id):
    project = Project.objects.get(id=id)
    if project.user != request.user:
        return redirect("/projects")

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

    form = TodoForm()
    todos = Todo.objects.filter(project=project)
    context = {
        "project": project,
        "todos": todos,
        "form": form,
    }
    return render(request, "todos.html", context)


def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("/projects/")
    else:
        form = ProjectForm()

    context = {
        "form": form,
    }
    return render(request, "new_project.html", context)


def edit_project(request, id):
    project = Project.objects.get(id=id)
    if project.user != request.user:
        return redirect("/projects")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("/projects/")
    else:
        form = ProjectForm(instance=project)

    context = {
        "form": form,
        "project": project,
    }
    return render(request, "edit_project.html", context)


def delete_project(request, id):
    project = Project.objects.get(id=id)
    if project.user != request.user:
        return redirect("/projects")

    if request.method == "POST":
        project.delete()
        return redirect("/projects/")
    else:
        form = ProjectDeleteForm()

    context = {
        "form": form,
        "project": project,
    }
    return render(request, "delete_project.html", context)


@login_not_required
def home(request):
    return render(request, "index.html", {})
