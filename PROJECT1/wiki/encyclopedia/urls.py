from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>",views.entry,name="entry"),
    path("random/", views.random, name="random"),
    path("add_entry/", views.add_entry, name="add_entry"),
    path("search/",views.search,name="search"),
    path("edit_entry/",views.edit_entry,name="edit_entry"),
    path("save_entry/", views.save_entry, name="save_entry"),
]
