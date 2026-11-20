import socket

from django.http import HttpResponse


def get_hostname(request):
    return HttpResponse(socket.gethostname(), content_type="text/plain; charset=utf-8")
