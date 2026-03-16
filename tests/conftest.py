"""Фикстуры для API-тестов"""

import pytest
import requests

from utils.data import BASE_URL, ENDPOINTS
from utils.helpers import generate_user_data


@pytest.fixture
def create_user():
    """Фикстура для создания пользователя с последующим удалением"""
    user_data = generate_user_data()
    
    response = requests.post(
        f"{BASE_URL}{ENDPOINTS['register']}",
        json=user_data
    )
    
    if response.status_code == 200:
        tokens = response.json()
        user_data["access_token"] = tokens.get("accessToken")
        user_data["refresh_token"] = tokens.get("refreshToken")
    
    yield user_data
    
    # Удаление пользователя после теста
    if user_data.get("access_token"):
        headers = {"Authorization": user_data["access_token"]}
        requests.delete(f"{BASE_URL}{ENDPOINTS['user']}", headers=headers)


@pytest.fixture
def get_ingredients():
    """Получение валидных хешей ингредиентов"""
    response = requests.get(f"{BASE_URL}{ENDPOINTS['ingredients']}")
    
    data = response.json()
    if data.get("success") and "data" in data:
        return [item["_id"] for item in data["data"]]
    return []