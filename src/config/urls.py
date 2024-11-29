from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import (
    UserActivationView,
    UserLogin,
    UserLogout,
    UserProfileView,
    UserRegistration,
    generate_accounts_view,
)
from common.views import IndexView
from games.views import (
    GenreDetailView,
    PlatformDetailView,
    generate_games_view,
    generate_reviews_view,
    generate_wishlist_view,
)

urlpatterns = (
    [
        path("", IndexView.as_view(), name="index"),
        path("registration/", UserRegistration.as_view(), name="registration"),
        path("accounts/", include("accounts.urls")),
        path("activate/<str:uuid64>/<str:token>/", UserActivationView.as_view(), name="activate_user"),
        path("login/", UserLogin.as_view(), name="login"),
        path("cart/", include("cart.urls")),
        path("logout/", UserLogout.as_view(), name="logout"),
        path("profile/", UserProfileView.as_view(), name="user_profile"),
        path("oauth/", include("social_django.urls", namespace="social")),
        path("admin/", admin.site.urls),
        path("games/", include("games.urls")),
        path("genres/<int:id>/", GenreDetailView.as_view(), name="genres_list"),
        path("platforms/<int:id>/", PlatformDetailView.as_view(), name="platforms_list"),
        path("api-auth/", include("rest_framework.urls")),
        path("api/", include("api.urls")),
        path("blog/", include("blog.urls")),
        path("generate_accounts/", generate_accounts_view, name="generate_accounts"),
        path("generate_games/", generate_games_view, name="generate_games"),
        path("generate_reviews/", generate_reviews_view, name="generate_reviews"),
        path("generate_wishlist/", generate_wishlist_view, name="generate_wishlist"),
    ]
    + debug_toolbar_urls()  # NOQA W503
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # NOQA W503
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOQA W503
)
