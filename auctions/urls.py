from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/follow", views.follow, name="follow"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/settle", views.settle, name="settle"),
    path("category/<str:category_name>", views.category, name="category")
]
