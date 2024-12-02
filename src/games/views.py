from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from games.forms import ReviewForm
from games.models import CompletedGames, Game, Genre, Platform, PurchaseHistory, Wishlist
from games.tasks import generate_games, generate_reviews, generate_wishlist


class AddToListMixin(View):
    model = None
    related_model = None
    redirect_url = None

    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        obj, created = self.related_model.objects.get_or_create(user=request.user, game=game)

        if created:
            message = "added to"
        else:
            message = "already in"

        messages.success(request, f"Game {game.title} has been {message} your list.")
        return redirect(self.redirect_url, pk=pk)


class AddToWishlistView(LoginRequiredMixin, AddToListMixin):
    related_model = Wishlist
    redirect_url = "games:game_detail"


class AddToCompletedGamesView(LoginRequiredMixin, AddToListMixin):
    related_model = CompletedGames
    redirect_url = "games:game_detail"


class RemoveFromListView(LoginRequiredMixin, View):
    model = None
    redirect_url = None

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        obj.delete()
        return redirect(self.redirect_url)


class RemoveFromWishlistView(RemoveFromListView):
    model = Wishlist
    redirect_url = "games:wishlist"


class RemoveFromCompletedGamesView(RemoveFromListView):
    model = CompletedGames
    redirect_url = "games:completed_games"


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
    try:
        count = int(request.GET.get("count", 100))
        if count <= 0:
            raise ValueError("Count must be a positive integer.")
        generate_games.delay("Game", count)
        return HttpResponse(f"Task to generate {count} games has started.")
    except ValueError as e:
        return HttpResponse(f"Invalid input: {str(e)}", status=400)


def generate_reviews_view(request):
    try:
        count = int(request.GET.get("count", 100))
        if count <= 0:
            raise ValueError("Count must be a positive integer.")
        generate_reviews.delay(count)
        return HttpResponse(f"Task to generate {count} reviews has started.")
    except ValueError as e:
        return HttpResponse(f"Invalid input: {str(e)}", status=400)


def generate_wishlist_view(request):
    try:
        count = int(request.GET.get("count", 100))
        if count <= 0:
            raise ValueError("Count must be a positive integer.")
        generate_wishlist.delay(count)
        return HttpResponse(f"Task to generate {count} wishlist entries has started.")
    except ValueError as e:
        return HttpResponse(f"Invalid input: {str(e)}", status=400)


def game_list(request):
    games = Game.objects.all()

    genre_id = request.GET.get("genre")
    if genre_id:
        games = games.filter(genre_id=genre_id)

    platform_id = request.GET.get("platform")
    if platform_id:
        games = games.filter(platform_id=platform_id)

    min_price = request.GET.get("min_price")
    if min_price:
        games = games.filter(price__gte=min_price)

    year = request.GET.get("year")
    if year:
        games = games.filter(release_year=year)

    paginator = Paginator(games, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    genres = Genre.objects.all()
    platforms = Platform.objects.all()

    return render(
        request,
        "game_list.html",
        {
            "games": page_obj,
            "genres": genres,
            "platforms": platforms,
            "selected_genre": genre_id,
            "selected_platform": platform_id,
            "min_price": min_price,
            "year": year,
        },
    )


def genre_detail(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    games = Game.objects.filter(genre=genre)

    platform_id = request.GET.get("platform")
    if platform_id:
        games = games.filter(platform_id=platform_id)

    paginator = Paginator(games, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    platforms = Platform.objects.all()

    return render(
        request,
        "genre_detail.html",
        {
            "genre": genre,
            "games": page_obj,
            "platforms": platforms,
            "selected_platform": platform_id,
        },
    )


def platform_detail(request, platform_id):
    platform = Platform.objects.get(id=platform_id)
    games = Game.objects.filter(platform=platform)

    genre_id = request.GET.get("genre")
    if genre_id:
        games = games.filter(genre_id=genre_id)

    paginator = Paginator(games, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    genres = Genre.objects.all()

    return render(
        request,
        "platform_detail.html",
        {
            "platform": platform,
            "games": page_obj,
            "genres": genres,
            "selected_genre": genre_id,
        },
    )
