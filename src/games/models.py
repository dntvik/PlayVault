from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField

from accounts.models import Customer
from games.utils.game_choises import GameСhoises


class Genre(models.Model):
    name = models.CharField(max_length=100, choices=GameСhoises.GENRE_CHOICES)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=100, choices=GameСhoises.PLATFORM_CHOICES)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    release_year = models.IntegerField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to="covers/")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    purchase_link = models.URLField()

    def __str__(self):
        return self.title


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user} on {self.game}"


class PurchaseHistory(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    price_at_purchase = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")

    def __str__(self):
        return f"{self.user} purchased {self.game} on {self.purchase_date} for {self.price_at_purchase}"


class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s wishlist: {self.game}"


class CompletedGames(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    completed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} completed {self.game} on {self.completed_date}"
