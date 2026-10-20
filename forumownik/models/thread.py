from django.contrib.auth.models import User
from django.db import models

from .category import Category


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.DB_CASCADE)
    author = models.ForeignKey(User, on_delete=models.DB_CASCADE)
    title = models.CharField(max_length=256)
    body = models.TextField()
    attachment = models.FileField(upload_to="threads/", null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Thread by {self.author.username} ID {self.id} in category {self.category.name}"
