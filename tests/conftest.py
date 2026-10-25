"""Фикстуры для API-тестов Stellar Burgers."""

import pytest
import requests

from utils.data import BASE_URL, ENDPOINTS
from utils.helpers import generate_user_data

REQUEST_TIMEOUT = 15


@pytest.fixture
def create_user():
    """Создать пользователя и удалить его после теста."""
    user_data = generate_user_data()
    response = requests.post(
        f"{BASE_URL}{ENDPOINTS['register']}",
        json=user_data,
        timeout=REQUEST_TIMEOUT,
    )
    assert response.status_code == 200, (
        f"Не удалось создать тестового пользователя: {response.status_code} "
        f"{response.text}"
    )
    payload = response.json()
    assert payload.get("accessToken"), "API не вернул accessToken"
    user_data["access_token"] = payload["accessToken"]
    user_data["refresh_token"] = payload.get("refreshToken")

    try:
        yield user_data
    finally:
        requests.delete(
            f"{BASE_URL}{ENDPOINTS['user']}",
            headers={"Authorization": user_data["access_token"]},
            timeout=REQUEST_TIMEOUT,
        )


@pytest.fixture
def get_ingredients():
    """Получить как минимум два валидных ингредиента."""
    response = requests.get(
        f"{BASE_URL}{ENDPOINTS['ingredients']}",
        timeout=REQUEST_TIMEOUT,
    )
    assert response.status_code == 200, (
        f"Не удалось получить ингредиенты: {response.status_code}"
    )
    payload = response.json()
    assert payload.get("success") is True, "API вернул ошибку получения ингредиентов"
    ingredients = [item["_id"] for item in payload["data"]]
    assert len(ingredients) >= 2, "Для тестов нужно не менее двух ингредиентов"
    return ingredients
