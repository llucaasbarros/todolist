from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class TaskModel(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, default="")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    category = models.ForeignKey(
        "categories.CategoryModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )

    is_completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)

    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "is_completed"]),
            models.Index(fields=["category"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return self.title


class TaskShareModel(TimeStampedModel):
    task = models.ForeignKey(
        "tasks.TaskModel",
        on_delete=models.CASCADE,
        related_name="shares",
    )

    shared_with = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shared_tasks",
    )

    shared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks_shared_by_me",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["task", "shared_with"], name="unique_task_share_per_user"
            ),
        ]

    def __str__(self):
        return f"{self.task} shared with {self.shared_with}"
