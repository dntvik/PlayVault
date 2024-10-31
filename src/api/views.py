from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CompletedGamesSerializer,
    GameSerializer,
    GenreSerializer,
    PlatformSerializer,
    PurchaseHistorySerializer,
    ReviewSerializer,
    WishlistSerializer,
)
from games.models import CompletedGames, Game, Genre, Platform, PurchaseHistory, Review, Wishlist


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GameListAPIView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GameRetrieveAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlatformListAPIView(ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlatformCreateView(CreateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class PlatformRetrieveView(RetrieveAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PlatformUpdateView(UpdateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class PlatformDeleteView(DestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewRetrieveAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PurchaseHistoryListAPIView(ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PurchaseHistory.objects.filter(user=user)


class PurchaseHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PurchaseHistory.objects.filter(user=user)


class WishlistListAPIView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)


class WishlistRetrieveAPIView(RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)


class CompletedGamesListAPIView(ListAPIView):
    serializer_class = CompletedGamesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CompletedGames.objects.filter(user=user)


class CompletedGamesRetrieveAPIView(RetrieveAPIView):
    serializer_class = CompletedGamesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CompletedGames.objects.filter(user=user)
