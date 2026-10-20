from django.contrib.auth.models import User
from django.db import models

from .thread import Thread


class ThreadVote(models.Model):
    pk = models.CompositePrimaryKey("thread", "user")
    thread = models.ForeignKey(Thread, on_delete=models.DB_CASCADE)
    user = models.ForeignKey(User, on_delete=models.DB_CASCADE)
    is_upvote = models.BooleanField()
