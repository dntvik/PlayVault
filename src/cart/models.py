from django.db import models
from djmoney.models.fields import MoneyField

from config.settings import base
from games.models import Game


class Cart(models.Model):
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField("CartItem", related_name="cart")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    def total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.price is None or self.quantity is None:
            raise ValueError("Price or quantity cannot be empty.")
        super().save(*args, **kwargs)
