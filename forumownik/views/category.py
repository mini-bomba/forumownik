from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render

from ..models import Category, Thread


def index(request):
    categories = Category.objects.annotate(threads=Count("thread")).order_by("id")
    return render(request, "category_index.html", {"categories": categories})


def show(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    threads = (
        Thread.objects.filter(category=category_id)
        .annotate(score=Sum("threadvote__score", default=0), comments=Count("comment"))
        .prefetch_related("author", "category")
        .order_by("-comments")
    )
    return render(
        request,
        "thread_list.html",
        {"threads": threads, "page_title": category.name, "page_header": f"Trending threads in {category.name}"},
    )
