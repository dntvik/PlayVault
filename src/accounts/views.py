from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, DetailView, RedirectView

from accounts.forms import UserRegistrationForm
from accounts.models import UserProfile
from accounts.tasks import generate_accounts
from accounts.utils.token_generators import TokenGenerator


def send_registration_email(user_instance, request):
    pass


class UserRegistration(CreateView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(user_instance=self.object, request=self.request)
        return super().form_valid(form)


class UserActivationView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data!!!")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)

            return super().get(request, *args, **kwargs)

        return HttpResponse("Wrong data!!!")


class UserLogin(LoginView):
    pass


class UserLogout(LogoutView):
    next_page = reverse_lazy("login")


class UserProfileView(DetailView):
    model = UserProfile
    template_name = "user_profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None


def generate_accounts_view(request: HttpRequest) -> HttpResponse:
    model_name = request.GET.get("model_name", "UserProfile")
    count = int(request.GET.get("count", 100))
    generate_accounts.delay(model_name, count)
    return HttpResponse(f"Task to generate {count} accounts in {model_name} is started.")
