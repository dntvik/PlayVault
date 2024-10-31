from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from games.models import CompletedGames, Game, Genre, Platform, PurchaseHistory, Review, Wishlist


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "genre",
            "platform",
            "release_year",
            "description",
            "cover_image",
            "purchase_link",
            "price",
        ]


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name"]


class ReviewSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Review
        fields = ["id", "game", "user", "rating", "comment"]


class PurchaseHistorySerializer(ModelSerializer):
    user = StringRelatedField()
    game = StringRelatedField()

    class Meta:
        model = PurchaseHistory
        fields = ["id", "user", "game", "purchase_date"]


class WishlistSerializer(ModelSerializer):
    user = StringRelatedField()
    game = StringRelatedField()

    class Meta:
        model = Wishlist
        fields = ["id", "user", "game"]


class CompletedGamesSerializer(ModelSerializer):
    user = StringRelatedField()
    game = StringRelatedField()

    class Meta:
        model = CompletedGames
        fields = ["id", "user", "game", "completed_date"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "birth_date", "photo", "date_joined", "is_active"]
