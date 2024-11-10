from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from games.models import CompletedGames, Game, Wishlist


class GameListView(ListView):
    model = Game
    template_name = "game_list.html"
    context_object_name = "games"


class GenreDetailView(ListView):
    model = Game
    template_name = "genres_list.html"
    context_object_name = "games"

    def get_queryset(self):
        return Game.objects.filter(genre_id=self.kwargs["id"])


class PlatformDetailView(ListView):
    model = Game
    template_name = "platforms_list.html"
    context_object_name = "games"

    def get_queryset(self):
        return Game.objects.filter(platform_id=self.kwargs["id"])


class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class CompletedGamesView(LoginRequiredMixin, ListView):
    model = CompletedGames
    template_name = "completed_games.html"
    context_object_name = "completed_games"

    def get_queryset(self):
        return CompletedGames.objects.filter(user=self.request.user)
