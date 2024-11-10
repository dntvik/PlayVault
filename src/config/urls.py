from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from common.views import IndexView
from games.views import GenreDetailView, PlatformDetailView

urlpatterns = [
                  path("", IndexView.as_view(), name="index"),
                  path("admin/", admin.site.urls),
                  path("games/", include("games.urls")),
                  path("genres/<int:id>/", GenreDetailView.as_view(), name="genres_list"),
                  path("platforms/<int:id>/", PlatformDetailView.as_view(), name="platforms_list"),
                  path("api-auth/", include("rest_framework.urls")),
                  path("api/", include("api.urls")),
                  path("blog/", include("blog.urls")),
              ] + debug_toolbar_urls() + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
