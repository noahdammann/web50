from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view, name="view"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit"),
    path("change/", views.change, name="change"),
    path("random/", views.get_random, name="random"),
]