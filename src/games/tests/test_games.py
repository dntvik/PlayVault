from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money

from games.models import CompletedGames, Game, Genre, Platform, Review, Wishlist


def create_sample_game(title="Sample Game", genre=None, platform=None, release_year=2020, price=Money(29.99, "USD")):
    game = Game.objects.create(
        title=title,
        release_year=release_year,
        description="Sample description",
        cover_image="covers/sample.jpg",
        price=price,
        purchase_link="https://example.com",
    )
    if genre:
        game.genre.set([genre])
    if platform:
        game.platform.set([platform])

    return game


class GameModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="testpassword123")
        self.genre = Genre.objects.create(name="Action")
        self.platform = Platform.objects.create(name="PC")
        self.game = create_sample_game(genre=self.genre, platform=self.platform)

    def test_game_creation(self):
        self.assertEqual(self.game.title, "Sample Game")
        self.assertEqual(self.game.genre.first().name, "Action")
        self.assertEqual(self.game.platform.first().name, "PC")
        self.assertEqual(float(self.game.price.amount), 29.99)
        self.assertEqual(self.game.price.currency.code, "USD")
        self.assertEqual(str(self.game), "Sample Game")


class GenreModelTest(TestCase):

    def test_genre_creation(self):
        genre, created = Genre.objects.get_or_create(name="Sport")
        self.assertTrue(created)
        self.assertEqual(str(genre), "Sport")


class PlatformModelTest(TestCase):

    def test_platform_creation(self):
        platform, created = Platform.objects.get_or_create(name="PLAYSTATION4")
        self.assertTrue(created)
        self.assertEqual(str(platform), "PLAYSTATION4")


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="testpassword123")
        self.genre = Genre.objects.create(name="Action")
        self.platform = Platform.objects.create(name="PC")
        self.game = create_sample_game(genre=self.genre, platform=self.platform)
        self.review = Review.objects.create(game=self.game, user=self.user, rating=8, comment="Great game!")

    def test_review_creation(self):
        self.assertEqual(self.review.game, self.game)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 8)
        self.assertEqual(self.review.comment, "Great game!")
        self.assertEqual(str(self.review), f"Review by {self.user} on {self.game}")


class WishlistAndCompletedGamesTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="testpassword123")
        self.genre = Genre.objects.create(name="Adventure")
        self.platform = Platform.objects.create(name="XBOX360")
        self.game = create_sample_game(
            title="Wishlisted Game", genre=self.genre, platform=self.platform, release_year=2021
        )

    def test_wishlist_creation(self):
        wishlist_item = Wishlist.objects.create(user=self.user, game=self.game)
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.game, self.game)
        self.assertEqual(str(wishlist_item), f"{self.user}'s wishlist: {self.game}")

    def test_completed_game_creation(self):
        completed_game = CompletedGames.objects.create(user=self.user, game=self.game, completed_date="2024-11-10")
        self.assertEqual(completed_game.user, self.user)
        self.assertEqual(completed_game.game, self.game)
        self.assertEqual(str(completed_game), f"{self.user} completed {self.game} on 2024-11-10")
