from django.urls import path

from accounts.views import EditProfileView

app_name = "accounts"

urlpatterns = [
    path("edit/<int:pk>/", EditProfileView.as_view(), name="edit_profile"),
]
