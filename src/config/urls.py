from debug_toolbar.toolbar import debug_toolbar_urls
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
] + debug_toolbar_urls()
