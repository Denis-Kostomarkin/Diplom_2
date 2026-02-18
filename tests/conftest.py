"""Фикстуры для API-тестов"""

import pytest
import requests

from utils.data import BASE_URL, ENDPOINTS
from utils.helpers import generate_user_data


@pytest.fixture
def base_url():
    """Базовый URL API"""
    return BASE_URL


@pytest.fixture
def endpoints():
    """Словарь эндпоинтов"""
    return ENDPOINTS


@pytest.fixture
def create_user(base_url, endpoints):
    """Фикстура для создания пользователя с последующим удалением"""
    user_data = generate_user_data()
    
    response = requests.post(
        f"{base_url}{endpoints['register']}",
        json=user_data
    )
    
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    
    tokens = response.json()
    user_data["access_token"] = tokens.get("accessToken")
    user_data["refresh_token"] = tokens.get("refreshToken")
    
    yield user_data
    
    if user_data.get("access_token"):
        headers = {"Authorization": user_data["access_token"]}
        requests.delete(f"{base_url}{endpoints['user']}", headers=headers)


@pytest.fixture
def get_ingredients(base_url, endpoints):
    """Получение валидных хешей ингредиентов"""
    response = requests.get(f"{base_url}{endpoints['ingredients']}")
    assert response.status_code == 200
    
    data = response.json()
    if data.get("success") and "data" in data:
        return [item["_id"] for item in data["data"]]
    return []