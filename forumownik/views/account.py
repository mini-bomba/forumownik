from django.contrib import auth
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django_ratelimit.decorators import ratelimit

from ..forms.account import LoginForm


def logout(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise BadRequest
    auth.logout(request)
    return redirect("global_trending")


@ratelimit(key='ip', rate='5/m', method=ratelimit.UNSAFE)
@ratelimit(key='post:username', rate='5/m', method=ratelimit.UNSAFE)
def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("global_trending")
    if request.method == "GET":
        form = LoginForm()
        if request.client_ip_routable:
            form.fields['captcha'].remote_ip = request.client_ip
        return render(request, "login.html", {"authuser": request.user, "form": form})
    if request.method != "POST":
        raise BadRequest

    form = LoginForm(request.POST)
    if request.client_ip_routable:
        form.fields['captcha'].remote_ip = request.client_ip

    if not form.is_valid():
        return render(request, "login.html", {"authuser": request.user, "form": form}, status=400)

    user = auth.authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    if user is None:
        form.add_error(None, "Invalid credentials")
        return render(request, "login.html", {"authuser": request.user, "form": form}, status=400)

    auth.login(request, user)
    target = request.GET.get("next")

    if target is None or not url_has_allowed_host_and_scheme(target):
        target = "global_trending"

    return redirect(target)
