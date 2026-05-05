from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item-list'),
    path('items/new/', views.ItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
]
