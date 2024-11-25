from celery import shared_task
from django.apps import apps
from faker import Faker

from accounts.models import UserProfile


@shared_task
def generate_accounts(model_name, count):
    faker = Faker("UK")
    Model = apps.get_model("accounts", "UserProfile")
    batch_size = 100

    for start in range(0, count, batch_size):
        end = min(start + batch_size, count)
        Model.objects.bulk_create(
            [
                Model(
                    title=faker.name(),
                    email=faker.unique.email(),
                    phone_number=faker.unique.phone_number(),
                    birth_date=faker.date_of_birth(minimum_age=18, maximum_age=65),
                )
                for _ in range(start, end)
            ]
        )
