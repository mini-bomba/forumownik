from django.urls import path

from . import views

urlpatterns = [path("", views.test.index, name="test")]
