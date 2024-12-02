from games.models import Genre, Platform
from games.utils.game_choises import GameСhoises


def add_genres_and_platforms():
    for genre_code, genre_name in GameСhoises.GENRE_CHOICES:
        Genre.objects.get_or_create(name=genre_code)

    for platform_code, platform_name in GameСhoises.PLATFORM_CHOICES:
        Platform.objects.get_or_create(name=platform_code)
