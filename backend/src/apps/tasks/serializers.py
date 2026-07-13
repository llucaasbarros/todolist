from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.categories.serializers import CategorySerializer
from apps.holidays import services as holidays_services

from .models import TaskModel, TaskShareModel

User = get_user_model()


class TaskShareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class TaskSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    is_owner = serializers.SerializerMethodField()
    shared_with = serializers.SerializerMethodField()
    due_date_is_holiday = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = (
            "id",
            "title",
            "description",
            "owner",
            "category",
            "category_detail",
            "is_completed",
            "due_date",
            "due_date_is_holiday",
            "priority",
            "is_owner",
            "shared_with",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("owner", "created_at", "updated_at")

    @extend_schema_field(serializers.BooleanField)
    def get_is_owner(self, obj):
        request = self.context.get("request")
        return bool(request and obj.owner_id == request.user.id)

    @extend_schema_field(TaskShareUserSerializer(many=True))
    def get_shared_with(self, obj):
        return TaskShareUserSerializer(
            [share.shared_with for share in obj.shares.all()], many=True
        ).data

    @extend_schema_field(serializers.BooleanField)
    def get_due_date_is_holiday(self, obj):
        if not obj.due_date:
            return False
        return holidays_services.is_holiday(obj.due_date)

    def validate_category(self, value):
        request = self.context.get("request")
        if value is not None and value.owner_id != request.user.id:
            raise serializers.ValidationError("Categoria inválida.")
        return value


class TaskShareSerializer(serializers.ModelSerializer):
    shared_with = TaskShareUserSerializer(read_only=True)
    shared_by = TaskShareUserSerializer(read_only=True)

    class Meta:
        model = TaskShareModel
        fields = ("id", "task", "shared_with", "shared_by", "created_at")
