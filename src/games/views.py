from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView

from games.models import CompletedGames, Game, Wishlist
from games.tasks import generate_games, generate_reviews, generate_wishlist


class GameListView(ListView):
    model = Game
    template_name = "game_list.html"
    context_object_name = "games"


class GenreDetailView(ListView):
    model = Game
    template_name = "genres_list.html"  # Создайте этот шаблон
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


def generate_games_view(request):
    count = int(request.GET.get("count", 100))
    generate_games.delay(count)
    return HttpResponse(f"Task to generate {count} games has started.")


def generate_reviews_view(request):
    count = int(request.GET.get("count", 100))
    generate_reviews.delay(count)
    return HttpResponse(f"Task to generate {count} reviews has started.")


def generate_wishlist_view(request):
    count = int(request.GET.get("count", 100))
    generate_wishlist.delay(count)
    return HttpResponse(f"Task to generate {count} wishlist entries has started.")
