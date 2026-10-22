from django.urls import path

from . import views

urlpatterns = [
    path("", views.global_trending.index, name="global_trending"),
    path("category", views.category.index, name="category_index"),
    path("category/<int:category_id>", views.category.show, name="category_show"),
    path("user/<int:user_id>", views.user.show, name="user_show"),
    path("thread/<int:thread_id>", views.thread.show, name="thread_show"),
    path("thread/<int:thread_id>/<int:comment_id>", views.thread.show_comment, name="comment_show"),
    path("404", views.error.page404, name="404"),
]

handler404 = "forumownik.views.error.page404"
