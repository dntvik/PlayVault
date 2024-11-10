from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsSuperUser
from api.serializers import (CompletedGamesSerializer, GameSerializer,
                             GenreSerializer, PlatformSerializer,
                             PurchaseHistorySerializer, ReviewSerializer,
                             WishlistSerializer)
from games.models import (CompletedGames, Game, Genre, Platform,
                          PurchaseHistory, Review, Wishlist)


class GenreViewAPISet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsSuperUser]


class GameViewAPISet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsSuperUser]


class GameListAPIView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlatformListAPIView(ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PlatformCreateAPIView(CreateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsSuperUser]


class PlatformRetrieveAPIView(RetrieveAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PlatformUpdateAPIView(UpdateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsSuperUser]


class PlatformDeleteAPIView(DestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsSuperUser]


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewRetrieveAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PurchaseHistoryListAPIView(ListAPIView):
    serializer_class = PurchaseHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return PurchaseHistory.objects.filter(user=user)


class PurchaseHistoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = PurchaseHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return PurchaseHistory.objects.filter(user=user)


class WishlistListAPIView(ListAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)


class WishlistRetrieveAPIView(RetrieveAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)


class CompletedGamesListAPIView(ListAPIView):
    serializer_class = CompletedGamesSerializer

    def get_queryset(self):
        user = self.request.user
        return CompletedGames.objects.filter(user=user)


class CompletedGamesRetrieveAPIView(RetrieveAPIView):
    serializer_class = CompletedGamesSerializer

    def get_queryset(self):
        user = self.request.user
        return CompletedGames.objects.filter(user=user)
