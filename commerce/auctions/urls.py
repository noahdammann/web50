from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("listing<int:listing_id>", views.listing_page, name="listing"),
    path("closed<int:listing_id>", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlistremove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category<str:categoryName>", views.category, name="category"),
    path("bid", views.bid, name="bid")
]
