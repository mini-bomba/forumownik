import socket

from django.http import HttpResponse


def get_hostname(request):
    return HttpResponse(socket.gethostname(), content_type="text/plain; charset=utf-8")


def get_ip(request):
    return HttpResponse(request.META.get("REMOTE_ADDR", "unknown"), content_type="text/plain; charset=utf-8")
