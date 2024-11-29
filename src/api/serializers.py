from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from cart.models import Cart, CartItem
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


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "birth_date", "photo", "date_joined", "is_active"]


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = [
            "id",
            "name",
        ]


class ReviewSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Review
        fields = ["id", "game", "user", "rating", "comment"]


class BaseGameInteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        fields = ["id", "user", "game"]


class WishlistSerializer(BaseGameInteractionSerializer):
    class Meta(BaseGameInteractionSerializer.Meta):
        model = Wishlist
        fields = BaseGameInteractionSerializer.Meta.fields


class CompletedGamesSerializer(BaseGameInteractionSerializer):
    class Meta(BaseGameInteractionSerializer.Meta):
        model = CompletedGames
        fields = BaseGameInteractionSerializer.Meta.fields + ["completed_date"]


class PurchaseHistorySerializer(BaseGameInteractionSerializer):
    class Meta(BaseGameInteractionSerializer.Meta):
        model = PurchaseHistory
        fields = BaseGameInteractionSerializer.Meta.fields + ["purchase_date", "price_at_purchase"]


class CartItemSerializer(serializers.ModelSerializer):
    game_title = serializers.ReadOnlyField(source="game.title")
    game_id = serializers.ReadOnlyField(source="game.id")

    class Meta:
        model = CartItem
        fields = ["id", "game_id", "game_title", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total"]

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
