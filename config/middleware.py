from ipware import get_client_ip

from . import settings


class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip, request.client_ip_routable = get_client_ip(
            request,
            proxy_count=settings.IPWARE_PROXY_COUNT,
            proxy_trusted_ips=settings.IPWARE_PROXY_IPS,
        )
        return self.get_response(request)
