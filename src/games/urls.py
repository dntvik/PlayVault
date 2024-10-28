from django.urls import path

from games.views import CompletedGamesView, GameListView, WishlistView

app_name = "games"

urlpatterns = [
    path("list/", GameListView.as_view(), name="game_list"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("completed-games/", CompletedGamesView.as_view(), name="completed_games"),
]
