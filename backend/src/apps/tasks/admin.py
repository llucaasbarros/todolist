from django.contrib import admin

from .models import TaskModel, TaskShareModel


@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "is_completed", "due_date", "priority")
    list_filter = ("is_completed", "priority", "category")
    search_fields = ("title", "description")


@admin.register(TaskShareModel)
class TaskShareModelAdmin(admin.ModelAdmin):
    list_display = ("task", "shared_with", "shared_by", "created_at")
    search_fields = ("task__title",)
