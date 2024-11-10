from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import UserLogin, UserLogout, UserProfileView, UserRegistration
from common.views import IndexView
from games.views import GenreDetailView, PlatformDetailView

urlpatterns = (
        [
            path("", IndexView.as_view(), name="index"),
            path("registration/", UserRegistration.as_view(), name="registration"),
            path("login/", UserLogin.as_view(), name="login"),
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
        ]
        + debug_toolbar_urls()  # NOQA W503
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # NOQA W503
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOQA W503
)
