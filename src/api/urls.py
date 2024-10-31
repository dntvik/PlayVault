from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CompletedGamesListAPIView,
    CompletedGamesRetrieveAPIView,
    GameListAPIView,
    GameRetrieveAPIView,
    GenreViewSet,
    PlatformCreateView,
    PlatformDeleteView,
    PlatformRetrieveView,
    PlatformUpdateView,
    PurchaseHistoryListAPIView,
    PurchaseHistoryRetrieveAPIView,
    ReviewListAPIView,
    ReviewRetrieveAPIView,
    WishlistListAPIView,
    WishlistRetrieveAPIView,
)

router = DefaultRouter()
router.register("genres", GenreViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("games/", GameListAPIView.as_view(), name="game-list"),
    path("games/<int:pk>/", GameRetrieveAPIView.as_view(), name="game-detail"),
    path("platform/create/", PlatformCreateView.as_view(), name="api_game_create"),
    path("platform/<int:pk>/", PlatformRetrieveView.as_view(), name="api_game_retrieve"),
    path("platform/<int:pk>/update/", PlatformUpdateView.as_view(), name="api_game_update"),
    path("platform/<int:pk>/delete/", PlatformDeleteView.as_view(), name="api_game_delete"),
    path("reviews/", ReviewListAPIView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewRetrieveAPIView.as_view(), name="review-detail"),
    path("purchase-history/", PurchaseHistoryListAPIView.as_view(), name="purchase-history-list"),
    path("purchase-history/<int:pk>/", PurchaseHistoryRetrieveAPIView.as_view(), name="purchase-history-detail"),
    path("wishlist/", WishlistListAPIView.as_view(), name="wishlist-list"),
    path("wishlist/<int:pk>/", WishlistRetrieveAPIView.as_view(), name="wishlist-detail"),
    path("completed-games/", CompletedGamesListAPIView.as_view(), name="completed-games-list"),
    path("completed-games/<int:pk>/", CompletedGamesRetrieveAPIView.as_view(), name="completed-games-detail"),
]
