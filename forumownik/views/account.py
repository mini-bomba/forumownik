from django.contrib import auth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect("global_trending")
