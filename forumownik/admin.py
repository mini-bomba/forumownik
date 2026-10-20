from django.contrib import admin

from .models import Category, Comment, Thread


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "category__name", "author", "title"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "reply_to__id", "author", "thread__title"]
