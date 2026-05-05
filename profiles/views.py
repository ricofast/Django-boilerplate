from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .forms import ProfileUpdateForm
from .models import Profile
from .permissions import IsSelfOrRoleAdmin
from .serializers import ProfileSerializer, UserSerializer

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        if self.request.user.is_role_admin and "pk" in self.kwargs:
            return Profile.objects.select_related("user").get(pk=self.kwargs["pk"])
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("profiles:profile-detail")

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsSelfOrRoleAdmin]

    def get_object(self):
        if self.request.user.is_role_admin and "pk" in self.kwargs:
            obj = self.get_queryset().get(pk=self.kwargs["pk"])
        else:
            obj, _ = Profile.objects.get_or_create(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
