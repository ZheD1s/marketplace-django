from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # Показывает только имя владельца

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'owner', 'created_at']