from unittest.mock import patch

import pytest
import requests

from apps.holidays import services

MOCK_HOLIDAYS_2026 = [
    {"date": "2026-01-01", "name": "Confraternização mundial", "type": "national"},
    {"date": "2026-04-21", "name": "Tiradentes", "type": "national"},
]


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"status {self.status_code}")


@patch("apps.holidays.services.requests.get")
def test_get_national_holidays_calls_external_api_and_caches(mock_get):
    mock_get.return_value = FakeResponse(MOCK_HOLIDAYS_2026)

    first = services.get_national_holidays(2026)
    second = services.get_national_holidays(2026)

    assert first == MOCK_HOLIDAYS_2026
    assert second == MOCK_HOLIDAYS_2026
    mock_get.assert_called_once()


@patch("apps.holidays.services.requests.get")
def test_is_holiday_true_for_matching_date(mock_get):
    mock_get.return_value = FakeResponse(MOCK_HOLIDAYS_2026)

    assert services.is_holiday("2026-01-01") is True
    assert services.is_holiday("2026-03-10") is False


@patch("apps.holidays.services.requests.get")
def test_is_holiday_returns_false_on_external_api_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("boom")

    assert services.is_holiday("2026-01-01") is False


@pytest.mark.django_db
@patch("apps.holidays.services.requests.get")
def test_holidays_view_returns_holidays_for_authenticated_user(mock_get, auth_client):
    mock_get.return_value = FakeResponse(MOCK_HOLIDAYS_2026)

    response = auth_client.get("/api/holidays/", {"year": 2026})

    assert response.status_code == 200
    assert response.data == MOCK_HOLIDAYS_2026


def test_holidays_view_requires_authentication(api_client):
    response = api_client.get("/api/holidays/", {"year": 2026})
    assert response.status_code == 401


@pytest.mark.django_db
def test_holidays_view_rejects_invalid_year(auth_client):
    response = auth_client.get("/api/holidays/", {"year": "not-a-year"})

    assert response.status_code == 400
    assert "year" in response.data


@pytest.mark.django_db
@patch("apps.holidays.services.requests.get")
def test_holidays_view_handles_upstream_failure(mock_get, auth_client):
    mock_get.side_effect = requests.exceptions.ConnectionError("boom")

    response = auth_client.get("/api/holidays/", {"year": 2026})

    assert response.status_code == 502
