import datetime

from django.contrib.auth.models import User
from django.db import models

from games.utils.game_choises import GameСhoises


class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, choices=GameСhoises.GENRE_CHOICES)
    platform = models.CharField(max_length=100, choices=GameСhoises.PLATFORM_CHOICES)
    release_year = models.IntegerField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to="covers/")
    purchase_link = models.URLField()


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
