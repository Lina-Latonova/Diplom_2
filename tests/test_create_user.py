import pytest
import requests
import allure
from constants import REGISTER_URL
from data.test_data import EXISTING_USER, INVALID_USER_PAYLOADS, ERROR_MESSAGES
from helpers import generate_unique_email

class TestCreateUser:
    @allure.title("Тест создания уникального пользователя")
    def test_create_unique_user(self):
        unique_email = generate_unique_email()
        password = "temp_password"
        name = "Temp User"

        register_payload = {
            "email": unique_email,
            "password": password,
            "name": name
        }

        # Шаг 1: Отправка POST-запроса на регистрацию
        with allure.step("Отправка POST-запроса для регистрации уникального пользователя"):
            response = requests.post(REGISTER_URL, json=register_payload)

        # Шаг 2: Проверка статуса ответа
        with allure.step(f"Проверка, что статус ответа равен 200. Получено: {response.status_code}"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Шаг 3: Проверка содержимого ответа и извлечение данных
        with allure.step("Проверка содержимого тела ответа и извлечение данных пользователя и токена"):
            response_data = response.json()
            user_data = response_data["user"]
            access_token = response_data["accessToken"]

            assert "user" in response_data, "Key 'user' not found in response"
            assert "accessToken" in response_data, "Key 'accessToken' not found in response"

        # Шаг 4: Проверка данных пользователя
        with allure.step("Проверка корректности данных созданного пользователя и токена"):
            assert 'email' in user_data
            assert 'name' in user_data
            assert '@example.com' in user_data['email']
            assert user_data['name'] == "Temp User"
            assert access_token is not None
            assert isinstance(access_token, str)
            assert access_token.startswith('Bearer ')

    @allure.title("Тест создания уже существующего пользователя")
    def test_create_existing_user(self):
        # Шаг 1: Отправка POST-запроса с данными существующего пользователя
        with allure.step("Отправка POST-запроса для регистрации существующего пользователя"):
            response = requests.post(REGISTER_URL, json=EXISTING_USER)

        # Шаг 2: Проверка статуса ответа (ожидается 403)
        with allure.step(f"Проверка, что статус ответа равен 403. Получено: {response.status_code}"):
            assert response.status_code == 403, f"Expected status code 403 for existing user, but got {response.status_code}. Response: {response.text}"

        # Шаг 3: Проверка содержимого ответа (ожидается ошибка)
        with allure.step("Проверка содержимого тела ответа на наличие сообщения об ошибке"):
            response_data = response.json()
            assert response_data.get('success') is False, f"Expected success: false, but got {response_data.get('success')}"
            assert 'message' in response_data, "Expected 'message' key in response"

            # Шаг 4: Проверка конкретного сообщения об ошибке
            with allure.step(f"Проверка, что сообщение об ошибке соответствует ожидаемому: '{ERROR_MESSAGES['USER_EXISTS']}'"):
                assert response_data['message'] == ERROR_MESSAGES["USER_EXISTS"], \
                    f"Message mismatch: Expected '{ERROR_MESSAGES['USER_EXISTS']}', but got '{response_data['message']}'"

    @allure.title("Тест создания пользователя с невалидными данными")
    @pytest.mark.parametrize("test_data,expected_message", INVALID_USER_PAYLOADS)
    def test_create_user_invalid_data(self, test_data, expected_message):
        # Шаг 1: Отправка POST-запроса с невалидными данными
        with allure.step(f"Отправка POST-запроса с невалидными данными: {test_data}"):
            response = requests.post(REGISTER_URL, json=test_data)

        # Шаг 2: Проверка статуса ответа (ожидается 403)
        with allure.step(f"Проверка, что статус ответа равен 403. Получено: {response.status_code}"):
            assert response.status_code == 403, f"Expected status code 403 for invalid data {test_data}, but got {response.status_code}. Response: {response.text}"

        # Шаг 3: Проверка содержимого ответа (ожидается ошибка)
        with allure.step("Проверка содержимого тела ответа на наличие сообщения об ошибке"):
            response_data = response.json()
            assert response_data.get('success') is False, f"Expected success: false for invalid data, but got {response_data.get('success')}"
            assert 'message' in response_data, "Expected 'message' key in response for invalid data"

            # Шаг 4: Проверка, что сообщение об ошибке содержит ожидаемую подстроку
            with allure.step(f"Проверка, что сообщение об ошибке содержит ожидаемую подстроку: '{expected_message}'"):
                assert expected_message.lower() in response_data['message'].lower(), \
                    f"Message mismatch for data {test_data}: Expected message to contain '{expected_message}', but got '{response_data['message']}'"
