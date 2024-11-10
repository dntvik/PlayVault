from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.serializers import PlatformSerializer
from api.views import (
    CompletedGamesListAPIView,
    CompletedGamesRetrieveAPIView,
    GameListAPIView,
    GameViewAPISet,
    GenreViewAPISet,
    PlatformCreateAPIView,
    PlatformDeleteAPIView,
    PlatformListAPIView,
    PlatformRetrieveAPIView,
    PlatformUpdateAPIView,
    PurchaseHistoryListAPIView,
    PurchaseHistoryRetrieveAPIView,
    ReviewListAPIView,
    ReviewRetrieveAPIView,
    WishlistListAPIView,
    WishlistRetrieveAPIView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register("genre", GenreViewAPISet)
router.register("games", GameViewAPISet)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("games-list/", GameListAPIView.as_view(), name="games-list"),
    path("platform/create/", PlatformCreateAPIView.as_view(), name="api_platform_create"),
    path("platform/list/", PlatformListAPIView.as_view(), name="api_platforms_list"),
    path("platform/<int:pk>/", PlatformRetrieveAPIView.as_view(), name="api_platform_retrieve"),
    path("platform/<int:pk>/update/", PlatformUpdateAPIView.as_view(), name="api_platform_update"),
    path("platform/<int:pk>/delete/", PlatformDeleteAPIView.as_view(), name="api_platform_delete"),
    path("reviews/", ReviewListAPIView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewRetrieveAPIView.as_view(), name="review-detail"),
    path("purchase-history/", PurchaseHistoryListAPIView.as_view(), name="purchase-history-list"),
    path("purchase-history/<int:pk>/", PurchaseHistoryRetrieveAPIView.as_view(), name="purchase-history-detail"),
    path("wishlist/", WishlistListAPIView.as_view(), name="wishlist-list"),
    path("wishlist/<int:pk>/", WishlistRetrieveAPIView.as_view(), name="wishlist-detail"),
    path("completed-games/", CompletedGamesListAPIView.as_view(), name="completed-games-list"),
    path("completed-games/<int:pk>/", CompletedGamesRetrieveAPIView.as_view(), name="completed-games-detail"),
]
