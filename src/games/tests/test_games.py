from django.contrib.auth import get_user_model
from django.test import TestCase

from games.models import CompletedGames, Game, Review, Wishlist


class GameModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model()(email="test@example.com")
        self.user.set_password("testpassword123")
        self.user.save()
        self.genre = "Action"
        self.platform = "PC"
        self.game = Game.objects.create(
            title="Test Game",
            genre=self.genre,
            platform=self.platform,
            release_year=2020,
            description="Test description",
            purchase_link="https://example.com",
        )

    def test_game_creation(self):
        self.assertEqual(self.game.title, "Test Game")
        self.assertEqual(self.game.genre, self.genre)
        self.assertEqual(self.game.platform, self.platform)
        self.assertEqual(self.game.release_year, 2020)
        self.assertEqual(str(self.game), "Test Game")


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model()(email="test@example.com")
        self.user.set_password("testpassword123")
        self.user.save()
        self.genre = "Action"
        self.platform = "PC"
        self.game = Game.objects.create(
            title="Test Game",
            genre=self.genre,
            platform=self.platform,
            release_year=2020,
            description="Test description",
            purchase_link="https://example.com",
        )
        self.review = Review.objects.create(game=self.game, user=self.user, rating=8, comment="Great game!")

    def test_review_creation(self):
        self.assertEqual(self.review.game, self.game)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 8)
        self.assertEqual(self.review.comment, "Great game!")
        self.assertEqual(str(self.review), f"Review by {self.user} on {self.game}")


class WishlistAndCompletedGamesTest(TestCase):
    def setUp(self):
        self.user = get_user_model()(email="test@example.com")
        self.user.set_password("testpassword123")
        self.user.save()
        self.genre = "Adventure"
        self.platform = "XBOX360"
        self.game = Game.objects.create(
            title="Wishlisted Game",
            genre=self.genre,
            platform=self.platform,
            release_year=2021,
            description="Wishlisted game description",
            purchase_link="https://example.com/wishlist",
        )

    def test_wishlist_creation(self):
        wishlist_item = Wishlist.objects.create(user=self.user, game=self.game)
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.game, self.game)
        self.assertEqual(str(wishlist_item), f"{self.user}'s wishlist: {self.game}")

    def test_completed_game_creation(self):
        completed_game = CompletedGames.objects.create(user=self.user, game=self.game)
        self.assertEqual(completed_game.user, self.user)
        self.assertEqual(completed_game.game, self.game)
        self.assertEqual(str(completed_game), f"{self.user} completed {self.game} on {completed_game.completed_date}")
