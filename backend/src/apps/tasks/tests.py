from unittest.mock import Mock, patch

import pytest

from apps.categories.models import CategoryModel
from apps.tasks.models import TaskModel, TaskShareModel


@pytest.mark.django_db
def test_create_task(auth_client, user):
    response = auth_client.post("/api/tasks/", {"title": "Comprar leite"}, format="json")

    assert response.status_code == 201
    assert response.data["owner"] == user.id
    assert response.data["is_owner"] is True
    assert response.data["is_completed"] is False
    assert response.data["priority"] == "medium"


@pytest.mark.django_db
def test_create_task_with_own_category(auth_client, user):
    category = CategoryModel.objects.create(name="Trabalho", owner=user)

    response = auth_client.post(
        "/api/tasks/", {"title": "Reunião", "category": category.id}, format="json"
    )

    assert response.status_code == 201
    assert response.data["category"] == category.id


@pytest.mark.django_db
def test_create_task_with_other_users_category_rejected(auth_client, other_user):
    other_category = CategoryModel.objects.create(name="Da outra pessoa", owner=other_user)

    response = auth_client.post(
        "/api/tasks/",
        {"title": "Tentando roubar categoria", "category": other_category.id},
        format="json",
    )

    assert response.status_code == 400
    assert "category" in response.data


@pytest.mark.django_db
def test_list_tasks_only_returns_own_and_shared(auth_client, user, other_user):
    TaskModel.objects.create(title="Minha tarefa", owner=user)
    TaskModel.objects.create(title="Tarefa de outro", owner=other_user)

    response = auth_client.get("/api/tasks/")

    titles = [item["title"] for item in response.data["results"]]
    assert titles == ["Minha tarefa"]


@pytest.mark.django_db
def test_toggle_task_completion(auth_client, user):
    task = TaskModel.objects.create(title="Tarefa", owner=user)

    response = auth_client.patch(f"/api/tasks/{task.id}/", {"is_completed": True}, format="json")

    assert response.status_code == 200
    assert response.data["is_completed"] is True


@pytest.mark.django_db
def test_delete_own_task(auth_client, user):
    task = TaskModel.objects.create(title="Tarefa", owner=user)

    response = auth_client.delete(f"/api/tasks/{task.id}/")

    assert response.status_code == 204
    assert not TaskModel.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_filter_tasks_by_is_completed(auth_client, user):
    TaskModel.objects.create(title="Pendente", owner=user, is_completed=False)
    TaskModel.objects.create(title="Concluída", owner=user, is_completed=True)

    response = auth_client.get("/api/tasks/", {"is_completed": "true"})

    titles = [item["title"] for item in response.data["results"]]
    assert titles == ["Concluída"]


@pytest.mark.django_db
def test_filter_tasks_by_category(auth_client, user):
    work = CategoryModel.objects.create(name="Trabalho", owner=user)
    personal = CategoryModel.objects.create(name="Pessoal", owner=user)
    TaskModel.objects.create(title="Tarefa de trabalho", owner=user, category=work)
    TaskModel.objects.create(title="Tarefa pessoal", owner=user, category=personal)

    response = auth_client.get("/api/tasks/", {"category": work.id})

    titles = [item["title"] for item in response.data["results"]]
    assert titles == ["Tarefa de trabalho"]


@pytest.mark.django_db
def test_filter_tasks_by_priority(auth_client, user):
    TaskModel.objects.create(title="Urgente", owner=user, priority="high")
    TaskModel.objects.create(title="Depois", owner=user, priority="low")

    response = auth_client.get("/api/tasks/", {"priority": "high"})

    titles = [item["title"] for item in response.data["results"]]
    assert titles == ["Urgente"]


@pytest.mark.django_db
def test_pagination_first_page(auth_client, user):
    for index in range(15):
        TaskModel.objects.create(title=f"Tarefa {index}", owner=user)

    response = auth_client.get("/api/tasks/")

    assert response.status_code == 200
    assert response.data["count"] == 15
    assert len(response.data["results"]) == 10
    assert response.data["next"] is not None
    assert response.data["previous"] is None


@pytest.mark.django_db
def test_pagination_second_page(auth_client, user):
    for index in range(15):
        TaskModel.objects.create(title=f"Tarefa {index}", owner=user)

    response = auth_client.get("/api/tasks/", {"page": 2})

    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    assert response.data["previous"] is not None
    assert response.data["next"] is None


@pytest.mark.django_db
def test_owner_can_share_task(auth_client, user, other_user):
    task = TaskModel.objects.create(title="Compartilhar", owner=user)

    response = auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": other_user.username}, format="json"
    )

    assert response.status_code == 201
    assert TaskShareModel.objects.filter(task=task, shared_with=other_user).exists()


@pytest.mark.django_db
def test_share_without_username_rejected(auth_client, user):
    task = TaskModel.objects.create(title="Compartilhar", owner=user)

    response = auth_client.post(f"/api/tasks/{task.id}/share/", {}, format="json")

    assert response.status_code == 400
    assert "username" in response.data


@pytest.mark.django_db
def test_owner_cannot_share_task_with_self(auth_client, user):
    task = TaskModel.objects.create(title="Compartilhar", owner=user)

    response = auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": user.username}, format="json"
    )

    assert response.status_code == 400
    assert "username" in response.data


@pytest.mark.django_db
def test_shared_user_sees_task_in_list(auth_client, other_auth_client, user, other_user):
    task = TaskModel.objects.create(title="Compartilhada", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = other_auth_client.get("/api/tasks/")

    titles = [item["title"] for item in response.data["results"]]
    assert titles == ["Compartilhada"]
    assert response.data["results"][0]["is_owner"] is False


@pytest.mark.django_db
def test_shared_user_cannot_edit_task(other_auth_client, user, other_user):
    task = TaskModel.objects.create(title="Compartilhada", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = other_auth_client.patch(
        f"/api/tasks/{task.id}/", {"title": "Hackeado"}, format="json"
    )

    assert response.status_code == 403
    task.refresh_from_db()
    assert task.title == "Compartilhada"


@pytest.mark.django_db
def test_shared_user_cannot_delete_task(other_auth_client, user, other_user):
    task = TaskModel.objects.create(title="Compartilhada", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = other_auth_client.delete(f"/api/tasks/{task.id}/")

    assert response.status_code == 403
    assert TaskModel.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_user_with_no_relation_to_task_gets_404_on_share(other_auth_client, user):
    """A task outside the requester's visibility scope (not owner, not shared)
    should 404, not 403 — avoids leaking that the task id exists at all."""
    task = TaskModel.objects.create(title="Não é minha", owner=user)

    response = other_auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": user.username}, format="json"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_shared_user_cannot_share_task_further(other_auth_client, user, other_user, create_user):
    """A user the task WAS shared with can see it (so get_object succeeds),
    but IsOwnerOrReadOnly still blocks the POST since they're not the owner."""
    third_user = create_user(username="thirduser")
    task = TaskModel.objects.create(title="Compartilhada", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = other_auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": third_user.username}, format="json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_cannot_share_task_twice_with_same_user(auth_client, user, other_user):
    task = TaskModel.objects.create(title="Tarefa", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": other_user.username}, format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_cannot_share_task_with_nonexistent_user(auth_client, user):
    task = TaskModel.objects.create(title="Tarefa", owner=user)

    response = auth_client.post(
        f"/api/tasks/{task.id}/share/", {"username": "fantasma"}, format="json"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_shared_with_field_reflects_shares(auth_client, user, other_user):
    task = TaskModel.objects.create(title="Tarefa", owner=user)
    TaskShareModel.objects.create(task=task, shared_with=other_user, shared_by=user)

    response = auth_client.get(f"/api/tasks/{task.id}/")

    usernames = [item["username"] for item in response.data["shared_with"]]
    assert usernames == [other_user.username]


def test_tasks_require_authentication(api_client):
    response = api_client.get("/api/tasks/")
    assert response.status_code == 401


@pytest.mark.django_db
@patch("apps.holidays.services.requests.get")
def test_due_date_is_holiday_flag(mock_get, auth_client):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"date": "2026-01-01", "name": "Confraternização mundial", "type": "national"}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    holiday_response = auth_client.post(
        "/api/tasks/", {"title": "Tarefa de feriado", "due_date": "2026-01-01"}, format="json"
    )
    normal_response = auth_client.post(
        "/api/tasks/", {"title": "Tarefa comum", "due_date": "2026-03-10"}, format="json"
    )

    assert holiday_response.data["due_date_is_holiday"] is True
    assert normal_response.data["due_date_is_holiday"] is False
