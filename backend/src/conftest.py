import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def create_user(db):
    def _create_user(username="testuser", email=None, password="SenhaForte123"):
        return User.objects.create_user(
            username=username,
            email=email or f"{username}@example.com",
            password=password,
        )

    return _create_user


@pytest.fixture
def user(create_user):
    return create_user()


@pytest.fixture
def other_user(create_user):
    return create_user(username="otheruser")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def other_auth_client(other_user):
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client
