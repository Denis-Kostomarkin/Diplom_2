"""Тесты регистрации пользователя."""

import allure
import pytest
import requests

from utils.data import BASE_URL, ENDPOINTS
from utils.helpers import generate_user_data

REQUEST_TIMEOUT = 15


@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("Регистрация уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['register']}",
            json=user_data,
            timeout=REQUEST_TIMEOUT,
        )
        try:
            assert response.status_code == 200
            payload = response.json()
            assert payload["success"] is True
            assert payload.get("accessToken")
            assert payload.get("refreshToken")
        finally:
            if response.status_code == 200:
                token = response.json().get("accessToken")
                if token:
                    requests.delete(
                        f"{BASE_URL}{ENDPOINTS['user']}",
                        headers={"Authorization": token},
                        timeout=REQUEST_TIMEOUT,
                    )

    @allure.title("Повторная регистрация существующего пользователя")
    def test_create_existing_user(self, create_user):
        duplicate_data = {
            "email": create_user["email"],
            "password": create_user["password"],
            "name": create_user["name"],
        }
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['register']}",
            json=duplicate_data,
            timeout=REQUEST_TIMEOUT,
        )
        assert response.status_code == 403
        assert response.json()["success"] is False

    @allure.title("Регистрация без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['register']}",
            json=user_data,
            timeout=REQUEST_TIMEOUT,
        )
        try:
            assert response.status_code == 403
            assert response.json()["success"] is False
        finally:
            if response.status_code == 200:
                token = response.json().get("accessToken")
                if token:
                    requests.delete(
                        f"{BASE_URL}{ENDPOINTS['user']}",
                        headers={"Authorization": token},
                        timeout=REQUEST_TIMEOUT,
                    )
