"""Тесты создания пользователя"""

import pytest
import requests
import allure

from utils.helpers import generate_user_data


@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("1. Создать уникального пользователя")
    def test_create_unique_user(self, base_url, endpoints):
        """Создание нового уникального пользователя"""
        user_data = generate_user_data()
        
        with allure.step("Отправка запроса на регистрацию"):
            response = requests.post(
                f"{base_url}{endpoints['register']}",
                json=user_data
            )
        
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data

    @allure.title("2. Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_user, base_url, endpoints):
        """Попытка создать дубликат пользователя"""
        existing_user = create_user
        
        duplicate_data = {
            "email": existing_user["email"],
            "password": existing_user["password"],
            "name": existing_user["name"]
        }
        
        with allure.step("Попытка создания дубликата"):
            response = requests.post(
                f"{base_url}{endpoints['register']}",
                json=duplicate_data
            )
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert response.json()["success"] is False

    @allure.title("3. Создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, base_url, endpoints, missing_field):
        """Создание пользователя без одного обязательного поля"""
        user_data = generate_user_data()
        del user_data[missing_field]
        
        with allure.step(f"Отправка запроса без поля {missing_field}"):
            response = requests.post(
                f"{base_url}{endpoints['register']}",
                json=user_data
            )
        
        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403
            assert response.json()["success"] is False