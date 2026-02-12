import pytest
import allure
import requests
import uuid
import logging
from data.test_data import TEST_USER
from constants import REGISTER_URL, LOGIN_URL, DELETE_URL

logger = logging.getLogger(__name__)

# Фикстура для получения токена авторизации
@pytest.fixture
def auth_token():
    login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}

    # Добавляем шаг для логирования получения токена
    with allure.step("Получение токена авторизации"):
        response = requests.post(LOGIN_URL, json=login_data)
        return response.json()["accessToken"]

# Фикстура для создания и удаления временного пользователя
@pytest.fixture
def temp_user():
    unique_email = f"temp_user_{uuid.uuid4()}@example.com"
    password = "temp_password"
    name = "Temp User"

    # Регистрация пользователя
    with allure.step("Регистрация временного пользователя"):
        register_response = requests.post(REGISTER_URL, json={
            "email": unique_email,
            "password": password,
            "name": name
        })
        response_data = register_response.json()
        user_data = response_data["user"]
        access_token = response_data["accessToken"]

    logger.info(f"Создан временный пользователь: {user_data['email']}")

    yield user_data, access_token

    # Удаление пользователя
    with allure.step("Удаление временного пользователя"):
        requests.delete(DELETE_URL, headers={"Authorization": f"Bearer {access_token}"})