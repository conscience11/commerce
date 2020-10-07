from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("listings/<int:pk>", views.listpage, name="listpage"),
    path("bid/<int:pk>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("addwatchlist/<int:pk>", views.add_watchlist, name="addwatchlist"),
    path("removewatchlist/<int:pk>", views.remove_watchlist, name="removewatchlist"),
    path("closelisting/<int:pk>", views.closelisting, name="closelisting"),
    path("won/<str:username>", views.won, name="won" ),
    path("won/<str:username>/<int:listid>", views.wonpage, name="wonpage"),
    path("closed/<str:username>", views.closed, name="closed"),
    path("closed/<str:username>/<int:listid>", views.clearclosed, name="clear")
]
