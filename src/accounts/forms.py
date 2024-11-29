from django.contrib.auth.forms import UserCreationForm

from accounts.models import Customer


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["username", "email", "phone_number", "birth_date", "photo", "password1", "password2"]
