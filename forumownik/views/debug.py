import socket

from django.http import HttpResponse


def get_hostname(request):
    return HttpResponse(socket.gethostname(), content_type="text/plain; charset=utf-8")


def get_ip(request):
    # nosemgrep: python.django.security.injection.reflected-data-httpresponse.reflected-data-httpresponse
    return HttpResponse(request.client_ip or "unknown", content_type="text/plain; charset=utf-8")
