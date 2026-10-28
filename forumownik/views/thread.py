import string
from random import SystemRandom

from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from django.db.models import Count, Prefetch, Sum
from django.shortcuts import get_object_or_404, redirect, render

from ..forms.thread import CreateCommentForm, CreateThreadForm
from ..models import Category, Comment, Thread

rng = SystemRandom()
FILENAME_CHARSET = string.ascii_letters + string.digits


def make_filename() -> str:
    return "".join(rng.choices(FILENAME_CHARSET, k=16))


def show(request, thread_id: int):
    qs = Thread.objects.annotate(score=Sum("threadvote__score", default=0), comments=Count("comment")).prefetch_related(
        "author", "category"
    )
    thread = get_object_or_404(qs, id=thread_id)

    # comments need to be formatted into a tree
    root_comments = (
        Comment.objects.filter(reply_to=None, thread_id=thread_id)
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


@login_required
def create_thread(request, category_id: int):
    c_qs = Category.objects.annotate(threads=Count("thread"))
    category = get_object_or_404(c_qs, id=category_id)

    if request.method == "GET":
        return render(
            request, "thread_create.html", {"authuser": request.user, "category": category, "form": CreateThreadForm()}
        )
    if request.method != "POST":
        raise BadRequest

    form = CreateThreadForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(
            request, "thread_create.html", {"authuser": request.user, "category": category, "form": form}, status=400
        )

    thread = Thread.objects.create(
        category=category,
        author=request.user,
        title=form.cleaned_data["title"],
        body=form.cleaned_data["body"],
    )
    attachment = form.cleaned_data["attachment"]
    if attachment is not None:
        thread.attachment.save(make_filename(), attachment)
    return redirect("thread_show", thread_id=thread.id)


@login_required
def create_root_comment(request, thread_id: int):
    thread_qs = Thread.objects.annotate(
        score=Sum("threadvote__score", default=0), comments=Count("comment")
    ).prefetch_related("author", "category")
    thread = get_object_or_404(thread_qs, id=thread_id)

    if request.method == "GET":
        return render(
            request, "thread_reply.html", {"authuser": request.user, "thread": thread, "form": CreateCommentForm()}
        )
    if request.method != "POST":
        raise BadRequest

    form = CreateCommentForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, "thread_reply.html", {"authuser": request.user, "thread": thread, "form": form}, status=400)

    comment = Comment.objects.create(
        thread=thread,
        author=request.user,
        body=form.cleaned_data["body"],
    )
    attachment = form.cleaned_data["attachment"]
    if attachment is not None:
        comment.attachment.save(make_filename(), attachment)
    return redirect("comment_show", thread_id=thread.id, comment_id=comment.id)


@login_required
def create_reply_comment(request, thread_id: int, comment_id: int):
    thread_qs = Thread.objects.annotate(
        score=Sum("threadvote__score", default=0), comments=Count("comment")
    ).prefetch_related("author", "category")
    qs = Comment.objects.annotate(score=Sum("commentvote__score", default=0)).prefetch_related(
        "author", Prefetch("thread", queryset=thread_qs)
    )
    comment = get_object_or_404(qs, id=comment_id, thread_id=thread_id)

    if request.method == "GET":
        return render(
            request,
            "thread_reply.html",
            {"authuser": request.user, "thread": comment.thread, "comment": comment, "form": CreateCommentForm()},
        )
    if request.method != "POST":
        raise BadRequest

    form = CreateCommentForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(
            request,
            "thread_reply.html",
            {"authuser": request.user, "thread": comment.thread, "comment": comment, "form": form},
            status=400,
        )

    new_comment = Comment.objects.create(
        thread=comment.thread,
        reply_to=comment,
        author=request.user,
        body=form.cleaned_data["body"],
    )
    attachment = form.cleaned_data["attachment"]
    if attachment is not None:
        new_comment.attachment.save(make_filename(), attachment)
    return redirect("comment_show", thread_id=comment.thread.id, comment_id=new_comment.id)
