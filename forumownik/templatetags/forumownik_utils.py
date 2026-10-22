import datetime
import re

from django import template
from django.db.models import Sum

from ..models import Comment

register = template.Library()
NEWLINE_REGEX = re.compile(r"[\r\n]+")
TIMEDELTA_THRESHOLD = datetime.timedelta(seconds=1)


@register.filter(is_safe=False)
def truncatelines(value, num):
    if not isinstance(num, int):
        raise TypeError("num should be an int")
    if num <= 0:
        raise ValueError("num must be > 0")
    if not isinstance(value, str):
        value = str(value)
    value = value.strip("\r\n")

    last_line = (0, 0)
    for i in range(num):
        match = NEWLINE_REGEX.search(value, last_line[1])
        if match is None:
            break
        last_line = match.span()
    else:
        value = f"{value[: last_line[0]]}…"

    return value


@register.filter(is_safe=False)
def wasedited(value):
    if not isinstance(value.posted_at, datetime.datetime):
        raise TypeError("posted_at is not a datetime")
    if not isinstance(value.edited_at, datetime.datetime):
        raise TypeError("edited_at is not a datetime")

    diff = abs(value.edited_at - value.posted_at)
    return diff > TIMEDELTA_THRESHOLD


@register.filter(is_safe=False)
def hasreplies(value):
    if not isinstance(value, Comment):
        raise TypeError("value should be a comment")
    return value.comment_set.exists()


@register.filter(is_safe=False)
def fetchreplies(value, orderby="posted_at"):
    if not isinstance(value, Comment):
        raise TypeError("value should be a comment")
    return (
        value.comment_set.annotate(score=Sum("commentvote__score", default=0)).prefetch_related("author").order_by(orderby)
    )
