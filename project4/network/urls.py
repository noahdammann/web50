
from django.urls import path

from . import views

urlpatterns = [
    # Pages
    path("", views.index, name="index"),

    # Data communication
    path("add", views.add, name="add"),
    path("posts/<str:feed>/<int:page>", views.send_feed, name="feed"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("post/<int:post_id>", views.post, name="edit_post"),
    path("like/<int:post_id>", views.like_post, name="like"),
    
    # Authentication 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
