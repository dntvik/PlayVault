from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from common.utils.token_generators import TokenGenerator


def send_registration_email(user_instance: get_user_model(), request: HttpRequest) -> None:
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    message = render_to_string(
        template_name="emails/registration.html",
        context={
            "user": user_instance,
            "domain": get_current_site(request),
            "token": TokenGenerator().make_token(user_instance),
            "uid": urlsafe_base64_encode(force_bytes(user_instance.id)),
            "current_time": current_time,
        },
    )

    email = EmailMessage(
        subject=settings.REGISTRATION_EMAIL_SUBJECT,
        body=message,
        to=[user_instance.email],
        cc=[settings.EMAIL_HOST_USER],
    )
    email.content_subtype = "html"
    email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
