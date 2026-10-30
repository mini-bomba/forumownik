import socket

from django.http import HttpResponse


def get_hostname(request):
    return HttpResponse(socket.gethostname())
