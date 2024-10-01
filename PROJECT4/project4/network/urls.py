
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post",views.add_post,name = "add_post"),
    path("profile/<int:user_id>",views.profile,name = "profile"),
    path("follow_toggle",views.follow_toggle,name = "follow_toggle"),
    path("following",views.following,name = "following"),
    path("edit/<int:post_id>", views.edit, name = "edit"),
]
