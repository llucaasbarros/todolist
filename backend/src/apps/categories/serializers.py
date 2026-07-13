from rest_framework import serializers

from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("id", "name", "color", "owner", "created_at", "updated_at")
        read_only_fields = ("owner", "created_at", "updated_at")

    def validate_name(self, value):
        request = self.context.get("request")
        queryset = CategoryModel.objects.filter(owner=request.user, name=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Você já tem uma categoria com esse nome.")
        return value
