from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.template import loader


@login_not_required
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context)
