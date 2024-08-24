from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>",views.entry,name="entry"),
    path("random/", views.random, name="random"),
    path("add_entry/", views.add_entry, name="add_entry"),
    path("search/",views.search,name="search")
]
