import pytest
import requests
import allure
from constants import LOGIN_URL
from data.test_data import LOGIN_USER, LOGIN_TEST_DATA, ERROR_MESSAGES

class TestLoginUser:

    @allure.title("Тест входа под существующим пользователем")
    def test_login_existing_user(self):
        login_data = {
            "email": LOGIN_USER["email"],
            "password": LOGIN_USER["password"]
        }

        # Шаг 1: Отправка POST-запроса на вход пользователя
        with allure.step("Отправка POST-запроса на вход существующего пользователя"):
            login_response = requests.post(LOGIN_URL, json=login_data)

        # Шаг 2: Проверка статуса ответа
        with allure.step(f"Проверка, что статус ответа равен 200. Получено: {login_response.status_code}"):
            assert login_response.status_code == 200, f"Expected status code 200, but got {login_response.status_code}"

        # Шаг 3: Проверка содержимого ответа
        with allure.step("Проверка содержимого тела ответа: success, accessToken, refreshToken, user"):
            response_json = login_response.json()
            assert response_json['success'] is True, f"Expected success: true, but got {response_json.get('success')}"
            assert 'accessToken' in response_json, "Key 'accessToken' not found in response"
            assert 'refreshToken' in response_json, "Key 'refreshToken' not found in response"
            assert 'user' in response_json, "Key 'user' not found in response"

            user_data = response_json['user']
            # Шаг 4: Проверка данных пользователя
            with allure.step("Проверка корректности данных пользователя (email, name)"):
                assert user_data['email'] == LOGIN_USER["email"], f"Email mismatch: Expected {LOGIN_USER['email']}, got {user_data.get('email')}"
                assert user_data['name'] == LOGIN_USER["name"], f"Name mismatch: Expected {LOGIN_USER['name']}, got {user_data.get('name')}"

    @allure.title("Тест входа с неверными учетными данными")
    def test_login_invalid_credentials(self):
        invalid_login_data = LOGIN_TEST_DATA["INVALID_CREDENTIALS"]

        # Шаг 1: Отправка POST-запроса с неверными учетными данными
        with allure.step(f"Отправка POST-запроса на вход с неверными данными: {invalid_login_data}"):
            invalid_response = requests.post(LOGIN_URL, json=invalid_login_data)

        # Шаг 2: Проверка статуса ответа (ожидается 401)
        with allure.step(f"Проверка, что статус ответа равен 401. Получено: {invalid_response.status_code}"):
            assert invalid_response.status_code == 401, f"Expected status code 401, but got {invalid_response.status_code}"

        # Шаг 3: Проверка содержимого ответа
        with allure.step("Проверка содержимого тела ответа: success и message"):
            response_json = invalid_response.json()
            assert response_json['success'] is False, f"Expected success: false, but got {response_json.get('success')}"

            # Шаг 4: Проверка конкретного сообщения об ошибке
            with allure.step(f"Проверка, что сообщение об ошибке соответствует ожидаемому: '{ERROR_MESSAGES['INVALID_CREDENTIALS']}'"):
                assert response_json['message'] == ERROR_MESSAGES["INVALID_CREDENTIALS"], \
                    f"Message mismatch: Expected '{ERROR_MESSAGES['INVALID_CREDENTIALS']}', but got '{response_json.get('message')}'"
