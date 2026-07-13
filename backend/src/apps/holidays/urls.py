from django.urls import path

from .views import HolidaysView

urlpatterns = [
    path("", HolidaysView.as_view(), name="holidays"),
]
