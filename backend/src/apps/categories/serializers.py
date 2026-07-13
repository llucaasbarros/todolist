from rest_framework import serializers

from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("id", "name", "color", "owner", "created_at", "updated_at")
        read_only_fields = ("owner", "created_at", "updated_at")
