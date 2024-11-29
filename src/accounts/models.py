from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomManager


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("name"), max_length=150, unique=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateTimeField(_("birth date"), null=True, blank=True)
    photo = models.ImageField(upload_to="users_avatars/", default="img/default_avatar.jpg", blank=True, null=True)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        return self.username

    def get_registration_duration(self):
        delta = timezone.now() - self.date_joined
        return f"Time on site: {delta.days} days, {delta.seconds // 3600} hours"
