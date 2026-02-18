"""Тесты логина пользователя"""

import pytest
import requests
import allure


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("1. Вход под существующим пользователем")
    def test_login_existing_user(self, create_user, base_url, endpoints):
        """Успешная авторизация"""
        user = create_user
        
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(
                f"{base_url}{endpoints['login']}",
                json=login_data
            )
        
        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data

    @allure.title("2. Вход с неверным логином и паролем")
    @pytest.mark.parametrize("wrong_field,wrong_value", [
        ("email", "wrong@email.com"),
        ("password", "wrong_password"),
    ])
    def test_login_with_wrong_credentials(self, create_user, base_url, endpoints, wrong_field, wrong_value):
        """Авторизация с неверными данными"""
        user = create_user
        
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        login_data[wrong_field] = wrong_value
        
        with allure.step(f"Отправка запроса с неверным {wrong_field}"):
            response = requests.post(
                f"{base_url}{endpoints['login']}",
                json=login_data
            )
        
        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()["success"] is False