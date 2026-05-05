from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'owner', 'owner_username', 'name', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'owner_username', 'created_at', 'updated_at']
