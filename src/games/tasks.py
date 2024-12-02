import random
from decimal import Decimal

import requests
from celery import shared_task
from django.apps import apps
from django.core.files.base import ContentFile
from faker import Faker

from games.models import Genre, Platform


@shared_task
def generate_games(model_name, count):
    faker = Faker()
    Model = apps.get_model("games", "Game")
    batch_size = 100

    for start in range(0, count, batch_size):
        end = min(start + batch_size, count)
        games = []

        for _ in range(start, end):
            response = requests.get("https://picsum.photos/400/600", stream=True)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                file_name = f"cover_{faker.uuid4()}.jpg"
            else:
                image_content = None
                file_name = None
            game = Model(
                title=faker.sentence(nb_words=3),
                genre=faker.random_element(Genre.objects.all()),
                platform=faker.random_element(Platform.objects.all()),
                release_year=faker.year(),
                description=faker.text(),
                price=Decimal(faker.random_number(digits=4)),
                purchase_link=faker.url(),
            )
            if image_content:
                game.cover_image.save(file_name, image_content, save=False)
            games.append(game)
        Model.objects.bulk_create(games)


@shared_task
def generate_reviews(count):
    faker = Faker()
    Review = apps.get_model("games", "Review")
    Game = apps.get_model("games", "Game")
    Customer = apps.get_model("accounts", "Customer")

    games = list(Game.objects.all())
    users = list(Customer.objects.all())

    if not games or not users:
        raise ValueError("There are no games or users available to create reviews.")

    batch_size = 100

    for start in range(0, count, batch_size):
        end = min(start + batch_size, count)
        reviews = []

        for _ in range(start, end):
            reviews.append(
                Review(
                    game=random.choice(games),
                    user=random.choice(users),
                    rating=random.randint(1, 10),
                    comment=faker.text(max_nb_chars=200),
                )
            )

        Review.objects.bulk_create(reviews)


@shared_task
def generate_wishlist(count):
    Wishlist = apps.get_model("games", "Wishlist")
    Game = apps.get_model("games", "Game")
    Customer = apps.get_model("accounts", "Customer")

    games = list(Game.objects.all())
    users = list(Customer.objects.all())

    if not games or not users:
        raise ValueError("There are no games or users available to create a wishlist.")

    batch_size = 100

    for start in range(0, count, batch_size):
        end = min(start + batch_size, count)
        wishlists = []

        for _ in range(start, end):
            user = random.choice(users)
            game = random.choice(games)

            if not Wishlist.objects.filter(user=user, game=game).exists():
                wishlists.append(
                    Wishlist(
                        user=user,
                        game=game,
                    )
                )

        Wishlist.objects.bulk_create(wishlists)
