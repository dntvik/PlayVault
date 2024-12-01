from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, RedirectView, UpdateView

from accounts.forms import UserRegistrationForm
from accounts.models import Customer
from accounts.services.emails import send_registration_email
from accounts.tasks import generate_accounts
from accounts.utils.token_generators import TokenGenerator


class UserRegistration(CreateView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(user_instance=self.object, request=self.request)
        messages.success(self.request, "Registration successful! Check your email to activate your account.")
        return super().form_valid(form)


class UserActivationView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            messages.error(request, "Invalid activation link!")
            return HttpResponse("Wrong data!!!")

        if current_user.is_active:
            messages.info(request, "Your account is already activated.")
            return HttpResponseRedirect(reverse("index"))

        if TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)
            messages.success(request, "Your account has been activated successfully!")
            return super().get(request, *args, **kwargs)

        # Если токен неверный
        messages.error(request, "Invalid activation link!")
        return HttpResponse("Wrong data!!!")


class UserLogin(LoginView):
    pass


class UserLogout(LogoutView):
    next_page = reverse_lazy("login")


class UserProfileView(DetailView):
    model = Customer
    template_name = "user_profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


class EditProfileView(UpdateView):
    model = Customer
    fields = ["username", "email", "phone_number", "birth_date", "photo"]
    template_name = "edit_profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        # Проверка на то, что редактируется профиль текущего пользователя
        return get_object_or_404(Customer, pk=self.request.user.pk)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


def generate_accounts_view(request: HttpRequest) -> HttpResponse:
    model_name = request.GET.get("model_name", "Customer")
    count = int(request.GET.get("count", 100))
    generate_accounts.delay(model_name, count)
    messages.info(request, f"Task to generate {count} accounts in {model_name} is started.")
    return HttpResponse(f"Task to generate {count} accounts in {model_name} is started.")
