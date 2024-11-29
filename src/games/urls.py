from django.urls import path

from cart.views import AddToCartView
from games.views import (
    AddReviewView,
    AddToCompletedGamesView,
    AddToWishlistView,
    CompletedGamesView,
    GameDetailView,
    GameListView,
    PurchaseHistoryView,
    RemoveFromCompletedGamesView,
    RemoveFromWishlistView,
    WishlistView,
)

app_name = "games"

urlpatterns = [
    path("", GameListView.as_view(), name="game_list"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("completed-games/", CompletedGamesView.as_view(), name="completed_games"),
    path("purchase_history/", PurchaseHistoryView.as_view(), name="purchase_history"),
    path("<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("<int:pk>/add_to_cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("<int:pk>/add_to_wishlist/", AddToWishlistView.as_view(), name="add_to_wishlist"),
    path("<int:pk>/add_to_completed_games/", AddToCompletedGamesView.as_view(), name="add_to_completed_games"),
    path("remove_from_wishlist/<int:item_pk>/", RemoveFromWishlistView.as_view(), name="remove_from_wishlist"),
    path(
        "remove_from_completed_games/<int:item_pk>/",
        RemoveFromCompletedGamesView.as_view(),
        name="remove_from_completed_games",
    ),
    path("<int:pk>/add-review/", AddReviewView.as_view(), name="add_review"),
]
