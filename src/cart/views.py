from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

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

        return Response(
            {"message": "Game added to cart", "cart_items_count": cart.items.count()}, status=status.HTTP_200_OK
        )


class RemoveFromCartAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)

        if (cart_item.cart.user and cart_item.cart.user != request.user) or (
            cart_item.cart.session_id and cart_item.cart.session_id != request.session.session_key
        ):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        context["cart"] = cart
        return context


class CheckoutView(TemplateView):
    template_name = "cart_checkout.html"


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, defaults={"price": game.price})

        if not created:
            cart_item.quantity = F("quantity") + 1
            cart_item.save()

        return redirect("games.game_detail", pk=game.pk)
