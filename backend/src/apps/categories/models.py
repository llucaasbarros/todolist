from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class CategoryModel(TimeStampedModel):
    name = models.CharField(max_length=100)

    color = models.CharField(max_length=7, blank=True, default="")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_category_name_per_owner"
            ),
        ]

    def __str__(self):
        return self.name
