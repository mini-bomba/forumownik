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
    path("account/logout", views.account.logout, name="account_logout"),
    path("account/login", views.account.login, name="account_login"),
    path("category/<int:category_id>/new_thread", views.thread.create_thread, name="thread_create"),
    path("thread/<int:thread_id>/reply", views.thread.create_root_comment, name="comment_create"),
    path("thread/<int:thread_id>/<int:comment_id>/reply", views.thread.create_reply_comment, name="comment_reply"),
    path("hostname", views.debug.get_hostname, name="hostname"),
]

handler404 = "forumownik.views.error.page404"
