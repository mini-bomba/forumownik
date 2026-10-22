from django.shortcuts import redirect, render


def handle404(request, exception=None):
    return redirect("404")


def page404(request):
    return render(request, "404.html", status=404)
