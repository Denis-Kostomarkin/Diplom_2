"""Тесты создания заказа"""

import pytest
import requests
import allure


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("1. Создание заказа с авторизацией")
    def test_create_order_with_auth(self, create_user, get_ingredients, base_url, endpoints):
        """Создание заказа с авторизацией"""
        user = create_user
        ingredients = get_ingredients
        
        order_data = {
            "ingredients": ingredients[:2] if len(ingredients) >= 2 else ingredients
        }
        headers = {"Authorization": user["access_token"]}
        
        with allure.step("Создание заказа с авторизацией"):
            response = requests.post(
                f"{base_url}{endpoints['orders']}",
                json=order_data,
                headers=headers
            )
        
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("2. Создание заказа без авторизации")
    def test_create_order_without_auth(self, get_ingredients, base_url, endpoints):
        """Создание заказа без авторизации"""
        ingredients = get_ingredients
        
        order_data = {
            "ingredients": ingredients[:2] if len(ingredients) >= 2 else ingredients
        }
        
        with allure.step("Создание заказа без авторизации"):
            response = requests.post(
                f"{base_url}{endpoints['orders']}",
                json=order_data
            )
        
        with allure.step("Проверка успешного создания (API позволяет без авторизации)"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("3. Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, create_user, get_ingredients, base_url, endpoints):
        """Создание заказа с ингредиентами"""
        user = create_user
        ingredients = get_ingredients
        
        order_data = {
            "ingredients": ingredients[:2] if len(ingredients) >= 2 else ingredients
        }
        headers = {"Authorization": user["access_token"]}
        
        with allure.step("Создание заказа с ингредиентами"):
            response = requests.post(
                f"{base_url}{endpoints['orders']}",
                json=order_data,
                headers=headers
            )
        
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("4. Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user, base_url, endpoints):
        """Создание заказа без ингредиентов"""
        user = create_user
        
        order_data = {"ingredients": []}
        headers = {"Authorization": user["access_token"]}
        
        with allure.step("Создание заказа без ингредиентов"):
            response = requests.post(
                f"{base_url}{endpoints['orders']}",
                json=order_data,
                headers=headers
            )
        
        with allure.step("Проверка ошибки 400"):
            assert response.status_code == 400
            assert response.json()["success"] is False

    @allure.title("5. Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash(self, create_user, base_url, endpoints):
        """Создание заказа с неверным хешем"""
        user = create_user
        
        order_data = {
            "ingredients": ["invalid_hash_12345"]
        }
        headers = {"Authorization": user["access_token"]}
        
        with allure.step("Создание заказа с неверным хешем"):
            response = requests.post(
                f"{base_url}{endpoints['orders']}",
                json=order_data,
                headers=headers
            )
        
        with allure.step("Проверка ошибки 500"):
            assert response.status_code == 500