
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("posts", views.all_posts, name="all_posts"),
    path("user/<int:user_id>", views.profile, name="profile"),
	path("follow/<int:user_id>", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("following", views.following, name="following"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/tweet", views.edit_tweet, name="editTweet"),
    path("like/tweet", views.like_tweet, name="likeTweet"),
    path("unlike/tweet", views.unlike_tweet, name="unlikeTweet"),
]
