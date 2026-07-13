import pytest

from apps.categories.models import CategoryModel


@pytest.mark.django_db
def test_create_category(auth_client, user):
    response = auth_client.post(
        "/api/categories/", {"name": "Trabalho", "color": "#338c96"}, format="json"
    )

    assert response.status_code == 201
    assert response.data["owner"] == user.id
    assert CategoryModel.objects.filter(name="Trabalho", owner=user).exists()


@pytest.mark.django_db
def test_list_categories_only_returns_own(auth_client, user, other_user):
    CategoryModel.objects.create(name="Minha categoria", owner=user)
    CategoryModel.objects.create(name="Categoria de outro", owner=other_user)

    response = auth_client.get("/api/categories/")

    names = [item["name"] for item in response.data["results"]]
    assert names == ["Minha categoria"]


@pytest.mark.django_db
def test_update_own_category(auth_client, user):
    category = CategoryModel.objects.create(name="Antigo", owner=user)

    response = auth_client.patch(f"/api/categories/{category.id}/", {"name": "Novo"}, format="json")

    assert response.status_code == 200
    category.refresh_from_db()
    assert category.name == "Novo"


@pytest.mark.django_db
def test_cannot_update_other_users_category(auth_client, other_user):
    category = CategoryModel.objects.create(name="Da outra pessoa", owner=other_user)

    response = auth_client.patch(
        f"/api/categories/{category.id}/", {"name": "Hackeado"}, format="json"
    )

    assert response.status_code == 404
    category.refresh_from_db()
    assert category.name == "Da outra pessoa"


@pytest.mark.django_db
def test_delete_own_category(auth_client, user):
    category = CategoryModel.objects.create(name="Excluir", owner=user)

    response = auth_client.delete(f"/api/categories/{category.id}/")

    assert response.status_code == 204
    assert not CategoryModel.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_cannot_delete_other_users_category(auth_client, other_user):
    category = CategoryModel.objects.create(name="Da outra pessoa", owner=other_user)

    response = auth_client.delete(f"/api/categories/{category.id}/")

    assert response.status_code == 404
    assert CategoryModel.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_duplicate_category_name_for_same_owner_rejected(auth_client, user):
    CategoryModel.objects.create(name="Duplicada", owner=user)

    response = auth_client.post(
        "/api/categories/", {"name": "Duplicada", "color": "#000000"}, format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_same_category_name_allowed_for_different_owners(auth_client, other_user):
    CategoryModel.objects.create(name="Compartilhado", owner=other_user)

    response = auth_client.post(
        "/api/categories/", {"name": "Compartilhado", "color": "#000000"}, format="json"
    )

    assert response.status_code == 201


def test_categories_require_authentication(api_client):
    response = api_client.get("/api/categories/")
    assert response.status_code == 401
