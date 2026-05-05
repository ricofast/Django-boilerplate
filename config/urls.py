from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from core.api_views import ItemViewSet

router = DefaultRouter()
router.register('items', ItemViewSet, basename='item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('core.urls')),
    path('api/', include(router.urls)),
]
