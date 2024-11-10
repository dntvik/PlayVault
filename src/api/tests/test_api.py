from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from games.models import Game, Genre, Platform

User = get_user_model()


class GameAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Action")
        self.platform = Platform.objects.create(name="PC")
        self.game = Game.objects.create(
            title="Test Game",
            release_year=2023,
            description="A test game description",
            price=59.99,
        )
        self.game.genre.set([self.genre])
        self.game.platform.set([self.platform])
        self.user = get_user_model()(email="user@example.com")
        self.user.set_password("qwerty1234")
        self.user.save()

    def test_game_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("games-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Game")

    def test_platforms_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api_platforms_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        self.assertEqual(response.data[0]["name"], "PC")

    def test_platforms_details_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api_platform_retrieve", args=[self.platform.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "PC")

    def test_review_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_wishlist_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("wishlist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
