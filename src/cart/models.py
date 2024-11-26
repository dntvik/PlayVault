from django.contrib.auth import get_user_model
from django.db import models
from djmoney.models.fields import MoneyField

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", blank=True, null=True)
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
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
