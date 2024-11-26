from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CartSerializer
from cart.models import Cart, CartItem
from games.models import Game


class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get("game_id")
        game = get_object_or_404(Game, id=game_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key or request.session.create()
            cart, created = Cart.objects.get_or_create(session_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, defaults={"price": game.price})
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({"message": "Game added to cart"}, status=status.HTTP_200_OK)


class RemoveFromCartAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)

        if cart_item.cart.user != request.user and cart_item.cart.session_id != request.session.session_key:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)


class CartAPIView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return get_object_or_404(Cart, user=self.request.user)
        else:
            session_id = self.request.session.session_key or self.request.session.create()
            return get_object_or_404(Cart, session_id=session_id)
