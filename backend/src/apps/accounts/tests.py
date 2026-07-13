import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_creates_user_with_hashed_password(api_client):
    response = api_client.post(
        "/api/auth/register/",
        {"username": "newuser", "email": "newuser@example.com", "password": "SenhaForte123"},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["username"] == "newuser"
    assert "password" not in response.data

    user = User.objects.get(username="newuser")
    assert user.password != "SenhaForte123"
    assert user.check_password("SenhaForte123")


@pytest.mark.django_db
def test_register_rejects_duplicate_username(api_client, user):
    response = api_client.post(
        "/api/auth/register/",
        {"username": user.username, "email": "another@example.com", "password": "SenhaForte123"},
        format="json",
    )

    assert response.status_code == 400
    assert "username" in response.data


@pytest.mark.django_db
def test_register_rejects_duplicate_email(api_client, user):
    response = api_client.post(
        "/api/auth/register/",
        {"username": "someoneelse", "email": user.email, "password": "SenhaForte123"},
        format="json",
    )

    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
def test_register_rejects_weak_password(api_client):
    response = api_client.post(
        "/api/auth/register/",
        {"username": "weakpass", "email": "weak@example.com", "password": "123"},
        format="json",
    )

    assert response.status_code == 400
    assert "password" in response.data


@pytest.mark.django_db
def test_login_returns_tokens_and_user(api_client, user):
    response = api_client.post(
        "/api/auth/login/",
        {"username": user.username, "password": "SenhaForte123"},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
    assert response.data["user"]["username"] == user.username


@pytest.mark.django_db
def test_login_rejects_wrong_password(api_client, user):
    response = api_client.post(
        "/api/auth/login/",
        {"username": user.username, "password": "wrong-password"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_login_rejects_nonexistent_user(api_client):
    response = api_client.post(
        "/api/auth/login/",
        {"username": "ghost", "password": "SenhaForte123"},
        format="json",
    )

    assert response.status_code == 401
