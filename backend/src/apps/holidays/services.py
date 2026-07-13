import requests
from django.core.cache import cache

BRASIL_API_URL = "https://brasilapi.com.br/api/feriados/v1/{year}"
CACHE_TTL_SECONDS = 60 * 60 * 24
CACHE_KEY_TEMPLATE = "holidays:{year}"


def get_national_holidays(year):
    cache_key = CACHE_KEY_TEMPLATE.format(year=year)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    response = requests.get(BRASIL_API_URL.format(year=year), timeout=5)
    response.raise_for_status()
    holidays = response.json()

    cache.set(cache_key, holidays, CACHE_TTL_SECONDS)
    return holidays


def is_holiday(date):
    date_str = date.isoformat() if hasattr(date, "isoformat") else date
    year = int(date_str[:4])
    try:
        holidays = get_national_holidays(year)
    except requests.exceptions.RequestException:
        return False
    return any(holiday["date"] == date_str for holiday in holidays)
