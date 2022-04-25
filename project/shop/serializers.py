from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category','shop', 'price', 'update_counter']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.update_counter += 1
        instance.save()
        return instance


