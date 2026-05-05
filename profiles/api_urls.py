from django.urls import path

from .views import CurrentUserAPIView, ProfileRetrieveUpdateAPIView

app_name = "profiles-api"

urlpatterns = [
    path("me/", CurrentUserAPIView.as_view(), name="current-user"),
    path("me/profile/", ProfileRetrieveUpdateAPIView.as_view(), name="my-profile"),
    path("profiles/<int:pk>/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
]
