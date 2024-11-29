from django.urls import path

from accounts.views import EditProfileView, UserProfileView, UserRegistration

app_name = "accounts"

urlpatterns = [
    path("edit/<int:pk>/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("registration/", UserRegistration.as_view(), name="registration"),
]
