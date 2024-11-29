from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from djmoney.models.fields import MoneyField

from config.settings import base
from games.models import Game

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    total_price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.game.price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
