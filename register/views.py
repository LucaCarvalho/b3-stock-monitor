from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Create your views here.

def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})