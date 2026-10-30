from django.contrib import auth
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms.account import LoginForm


def logout(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise BadRequest
    auth.logout(request)
    return redirect("global_trending")


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("global_trending")
    if request.method == "GET":
        return render(request, "login.html", {"authuser": request.user, "form": LoginForm()})
    if request.method != "POST":
        raise BadRequest

    form = LoginForm(request.POST)

    if not form.is_valid():
        return render(request, "login.html", {"authuser": request.user, "form": form}, status=400)

    user = auth.authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    if user is None:
        form.add_error(None, "Invalid credentials")
        return render(request, "login.html", {"authuser": request.user, "form": form}, status=400)

    auth.login(request, user)
    return redirect(request.GET.get("next", "global_trending"))
