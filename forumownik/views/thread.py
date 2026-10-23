from django.db.models import Count, Prefetch, Sum
from django.shortcuts import get_object_or_404, render

from ..models import Comment, Thread


def show(request, thread_id: int):
    qs = Thread.objects.annotate(score=Sum("threadvote__score", default=0), comments=Count("comment")).prefetch_related(
        "author", "category"
    )
    thread = get_object_or_404(qs, id=thread_id)

    # comments need to be formatted into a tree
    root_comments = (
        Comment.objects.filter(reply_to=None)
        .annotate(score=Sum("commentvote__score", default=0))
        .prefetch_related("author")
        .order_by("posted_at")
    )

    return render(
        request,
        "thread_show.html",
        {"thread": thread, "comments": root_comments, "authuser": request.user},
    )


def show_comment(request, thread_id: int, comment_id: int):
    thread_qs = Thread.objects.annotate(
        score=Sum("threadvote__score", default=0), comments=Count("comment")
    ).prefetch_related("author", "category")
    reply_qs = Comment.objects.annotate(score=Sum("commentvote__score", default=0))
    qs = Comment.objects.annotate(score=Sum("commentvote__score", default=0)).prefetch_related(
        "author", Prefetch("thread", queryset=thread_qs), Prefetch("reply_to", queryset=reply_qs)
    )
    comment = get_object_or_404(qs, id=comment_id, thread_id=thread_id)

    return render(request, "thread_show.html", {"thread": comment.thread, "comment": comment, "authuser": request.user})
