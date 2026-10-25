# Stellar Burgers — API Test Automation

Учебный проект по автоматизированному тестированию REST API сервиса [Stellar Burgers](https://stellarburgers.education-services.ru).

> **Статус:** проект разработан для учебного окружения. Текущая доступность стенда и успешность запуска тестов не подтверждены.

## Технологии

- Python
- Pytest
- Requests
- Allure Pytest

## Покрытые сценарии

**Регистрация пользователей**
- Создание уникального пользователя.
- Запрет повторной регистрации существующего пользователя.
- Проверка обязательных полей: email, пароль, имя.

**Авторизация**
- Вход с корректными учётными данными.
- Отказ во входе с неверным email или паролем.

**Создание заказов**
- Создание заказа с авторизацией и без неё.
- Создание заказа с ингредиентами.
- Ошибка при пустом списке ингредиентов.
- Поведение API при некорректном идентификаторе ингредиента.

> В учебной версии API для некорректного идентификатора ингредиента ожидается HTTP 500. В промышленном API это обычно рассматривалось бы как дефект обработки некорректного ввода; тест сохраняет ожидаемое поведение учебного стенда.

## Структура

```text
Diplom_2/
├── tests/
│   ├── conftest.py
│   ├── test_user_create.py
│   ├── test_user_login.py
│   └── test_order_create.py
├── utils/
│   ├── data.py
│   └── helpers.py
├── requirements.txt
└── README.md
```

- `tests/` — тестовые сценарии и фикстуры для подготовки данных и очистки после тестов.
- `utils/data.py` — базовый URL и маршруты API.
- `utils/helpers.py` — генерация тестовых пользователей.

## Установка

```bash
git clone https://github.com/Denis-Kostomarkin/Diplom_2.git
cd Diplom_2
python -m venv .venv
```

Активация окружения в Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
pytest tests/ -v
```

Запуск с формированием данных Allure:

```bash
pytest tests/ -v --alluredir=allure-results
```

При установленном Allure CLI:

```bash
allure serve allure-results
```

## Особенности

- Позитивные и негативные API-сценарии.
- Параметризация проверок обязательных полей и неверных учётных данных.
- Генерация уникальных тестовых пользователей.
- Фикстуры для создания и удаления тестовых пользователей.
- Проверки HTTP-статусов и полей JSON-ответов.

## Автор

[Denis-Kostomarkin](https://github.com/Denis-Kostomarkin)
