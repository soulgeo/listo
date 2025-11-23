from django import forms
from django.forms import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class ProjectDeleteForm(forms.Form):
    hidden = forms.HiddenInput()


class TodoForm(forms.Form):
    name = forms.CharField(max_length=255)
