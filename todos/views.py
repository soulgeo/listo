from django.http import HttpResponse
from django.template import loader

from .models import Project


def projects(request):
    template = loader.get_template("projects.html")
    projects = Project.objects.all().values()
    context = {"projects": projects}
    return HttpResponse(template.render(context, request))
