from django.contrib.auth.models import User
from django.db import models

from .comment import Comment


class CommentVote(models.Model):
    pk = models.CompositePrimaryKey("comment", "user")
    comment = models.ForeignKey(Comment, on_delete=models.DB_CASCADE)
    user = models.ForeignKey(User, on_delete=models.DB_CASCADE)
    is_upvote = models.BooleanField()
