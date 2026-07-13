from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import TaskModel, TaskShareModel
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer, TaskShareSerializer

User = get_user_model()


class TaskViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = TaskSerializer
    filterset_fields = ("is_completed", "category", "priority")

    def get_queryset(self):
        user = self.request.user
        return (
            TaskModel.objects.filter(Q(owner=user) | Q(shares__shared_with=user))
            .distinct()
            .prefetch_related("shares__shared_with")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="share")
    def share(self, request, pk=None):
        task = self.get_object()
        if task.owner_id != request.user.id:
            return Response(
                {"detail": "Apenas o dono pode compartilhar a tarefa."},
                status=status.HTTP_403_FORBIDDEN,
            )

        username = request.data.get("username")
        if not username:
            return Response(
                {"username": "Informe o nome de usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"username": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if target_user.id == task.owner_id:
            return Response(
                {"username": "Você já é o dono desta tarefa."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        share, created = TaskShareModel.objects.get_or_create(
            task=task, shared_with=target_user, defaults={"shared_by": request.user}
        )
        if not created:
            return Response(
                {"detail": "Tarefa já compartilhada com este usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(TaskShareSerializer(share).data, status=status.HTTP_201_CREATED)
