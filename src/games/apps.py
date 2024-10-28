from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PlayvaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "games"


class YourAppConfig(AppConfig):
    name = "games"

    def ready(self):
        from games.utils.add_genres_platforms import add_genres_and_platforms

        post_migrate.connect(run_populate_data, sender=self)


def run_populate_data(sender, **kwargs):
    from games.utils.add_genres_platforms import add_genres_and_platforms

    add_genres_and_platforms()
