from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render

from ..models import Thread


def show(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    threads = (
        Thread.objects.filter(author=user_id)
        .annotate(score=Sum("threadvote__score", default=0), comments=Count("comment"))
        .prefetch_related("author", "category")
        .order_by("-posted_at")
    )
    return render(
        request,
        "user_show.html",
        {"threads": threads, "user": user, "authuser": request.user},
    )
