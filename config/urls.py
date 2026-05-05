from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.api_views import ItemViewSet


router = DefaultRouter()
router.register("items", ItemViewSet, basename="item")


def health(request):
    return JsonResponse({"status": "ok", "user": str(request.user)})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profiles/", include("profiles.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/", include(router.urls)),
    path("health/", health, name="health"),
    path("", include("core.urls")),
]
