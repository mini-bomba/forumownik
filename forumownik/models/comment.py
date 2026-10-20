from django.contrib.auth.models import User
from django.db import models

from .thread import Thread


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.DB_CASCADE)
    reply_to = models.ForeignKey("self", on_delete=models.DB_CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.DB_CASCADE)
    body = models.TextField()
    attachment = models.FileField(upload_to="comments/", null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Comment by {self.author.username} ID {self.id} on thread {self.thread.id}"
