from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView

app_name = "profiles"

urlpatterns = [
    path("me/", ProfileDetailView.as_view(), name="profile-detail"),
    path("me/edit/", ProfileUpdateView.as_view(), name="profile-update"),
]
