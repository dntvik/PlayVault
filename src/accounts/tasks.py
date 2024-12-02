from celery import shared_task
from django.apps import apps
from django.utils import timezone
from faker import Faker


@shared_task
def generate_accounts(model_name, count):
    faker = Faker("UK")
    Model = apps.get_model("accounts", "Customer")
    batch_size = 100

    for start in range(0, count, batch_size):
        end = min(start + batch_size, count)
        Model.objects.bulk_create(
            [
                Model(
                    username=faker.name(),
                    email=faker.unique.email(),
                    phone_number=faker.unique.phone_number(),
                    birth_date=faker.date_of_birth(minimum_age=18, maximum_age=65),
                )
                for _ in range(start, end)
            ]
        )
