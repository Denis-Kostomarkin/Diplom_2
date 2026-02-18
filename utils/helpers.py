"""Вспомогательные функции"""

import random
import string


def generate_random_string(length=10):
    """Генерация случайной строки"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email():
    """Генерация случайного email"""
    return f"{generate_random_string(8)}@{generate_random_string(5)}.com"


def generate_user_data():
    """Генерация данных для нового пользователя"""
    return {
        "email": generate_random_email(),
        "password": "password123",
        "name": f"User_{generate_random_string(5)}"
    }