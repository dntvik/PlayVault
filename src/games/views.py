from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from games.forms import ReviewForm
from games.models import CompletedGames, Game, PurchaseHistory, Wishlist
from games.tasks import generate_games, generate_reviews, generate_wishlist


class GameListView(ListView):
    model = Game
    template_name = "game_list.html"
    context_object_name = "games"


class GameDetailView(DetailView):
    model = Game
    template_name = "game_detail.html"
    context_object_name = "game"


class GenreDetailView(ListView):
    model = Game
    template_name = "genres_detail.html"
    context_object_name = "games"

    def get_queryset(self):
        return Game.objects.filter(genre_id=self.kwargs["id"])


class PlatformDetailView(ListView):
    model = Game
    template_name = "platforms_detail.html"
    context_object_name = "games"

    def get_queryset(self):
        return Game.objects.filter(platform_id=self.kwargs["id"])


class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class PurchaseHistoryView(ListView):
    model = PurchaseHistory
    template_name = "purchase_history.html"
    context_object_name = "purchase_history"

    def get_queryset(self):
        return PurchaseHistory.objects.filter(user=self.request.user)


class CompletedGamesView(LoginRequiredMixin, ListView):
    model = CompletedGames
    template_name = "completed_games.html"
    context_object_name = "completed_games"

    def get_queryset(self):
        return CompletedGames.objects.filter(user=self.request.user)


class AddReviewView(LoginRequiredMixin, FormView):
    template_name = "game_detail.html"
    form_class = ReviewForm

    def form_valid(self, form):
        game = get_object_or_404(Game, pk=self.kwargs["pk"])
        review = form.save(commit=False)
        review.game = game
        review.user = self.request.user
        review.save()
        return redirect("games:game_detail", pk=game.pk)


def generate_games_view(request):
    count = int(request.GET.get("count", 100))
    generate_games.delay("Game", count)
    return HttpResponse(f"Task to generate {count} games has started.")


def generate_reviews_view(request):
    count = int(request.GET.get("count", 100))
    generate_reviews.delay(count)
    return HttpResponse(f"Task to generate {count} reviews has started.")


def generate_wishlist_view(request):
    count = int(request.GET.get("count", 100))
    generate_wishlist.delay(count)
    return HttpResponse(f"Task to generate {count} wishlist entries has started.")


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, game=game)
        return redirect("games:game_detail", pk=pk)


# Добавить в Completed Games
class AddToCompletedGamesView(LoginRequiredMixin, View):
    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        completed_game, created = CompletedGames.objects.get_or_create(user=request.user, game=game)
        return redirect("games:game_detail", pk=pk)


class RemoveFromCompletedGamesView(LoginRequiredMixin, View):
    def post(self, request, pk):
        completed_game = get_object_or_404(CompletedGames, pk=pk, user=request.user)
        completed_game.delete()
        return redirect("games:completed_games")


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist_item.delete()
        return redirect("games:wishlist")
