from django.db.models import Count, Sum
from django.shortcuts import render

from ..models import Thread


def index(request):
    threads = (
        Thread.objects.annotate(score=Sum("threadvote__score", default=0), comments=Count("comment"))
        .prefetch_related("author", "category")
        .order_by("-posted_at")
    )
    return render(
        request,
        "global.html",
        {"threads": threads, "page_title": "Global trending", "page_header": "Trending threads", "authuser": request.user},
    )
