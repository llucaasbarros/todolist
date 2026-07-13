from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import CategoryModel
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryModel.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
