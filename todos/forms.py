from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(label="Name", max_length=255)
    description = forms.CharField(label="Description")


class ProjectDeleteForm(forms.Form):
    hidden = forms.HiddenInput()
