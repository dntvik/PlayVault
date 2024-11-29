from datetime import timedelta
from decimal import InvalidOperation

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from games.models import Game


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key or request.session.create()
        cart, _ = Cart.objects.get_or_create(session_id=session_id)

        # Очистка корзины для анонимных пользователей, если она старше 30 минут
        if cart.updated_at < timezone.now() - timedelta(minutes=30):
            cart.items.all().delete()
            cart.save()

    return cart


class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get("game_id")
        game = get_object_or_404(Game, id=game_id)

        cart = get_or_create_cart(request)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, defaults={"price": game.price})

        if not created:
            cart_item.quantity = F("quantity") + 1
            cart_item.save()

        return Response(
            {"message": "Game added to cart", "cart_items_count": cart.items.count()},
            status=status.HTTP_200_OK,
        )


class RemoveFromCartAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        cart_item = get_object_or_404(CartItem, id=item_id)

        if (cart_item.cart.user and cart_item.cart.user != request.user) or (
            cart_item.cart.session_id and cart_item.cart.session_id != request.session.session_key
        ):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()

        if cart:
            cart_total = cart.items.aggregate(total=Sum(F("total_price")))["total"] or 0
            context["cart_total"] = cart_total

        context["cart"] = cart
        return context


class CheckoutView(TemplateView):
    template_name = "cart_checkout.html"


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)

        if not game.price or game.price.amount <= 0:
            return HttpResponse("Invalid price for the game", status=400)

        try:
            cart = get_or_create_cart(request)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, defaults={"price": game.price})

            if not created:
                cart_item.quantity = F("quantity") + 1
                cart_item.save()
                cart_item.refresh_from_db()

            messages.success(request, f"'{game.name}' has been added to your cart!")
        except InvalidOperation as e:
            return HttpResponse(f"Error when adding to cart: {repr(e)}", status=400)

        return redirect("games:game_detail", pk=pk)


class UpdateCartItemAPIView(APIView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        quantity = request.data.get("quantity")

        if quantity <= 0:
            return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Cart item updated", "cart_items_count": cart_item.cart.items.count()})


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=item_id)

        if cart_item.cart.user != request.user:
            return HttpResponse("Permission denied", status=403)

        cart_item.delete()
        messages.success(request, "Item removed from cart")
        return redirect("cart:cart")
