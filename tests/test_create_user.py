import pytest
import requests
import allure
import uuid
from constants import REGISTER_URL
from data.test_data import EXISTING_USER, INVALID_USER_PAYLOADS, ERROR_MESSAGES

class TestCreateUser:
    @allure.title("Тест создания уникального пользователя")
    def test_create_unique_user(self):
        unique_email = f"temp_user_{uuid.uuid4()}@example.com"
        password = "temp_password"
        name = "Temp User"
        
        # Шаг 1: Отправка запроса на регистрацию
        register_payload = {
            "email": unique_email,
            "password": password,
            "name": name}
        response = requests.post(REGISTER_URL, json=register_payload)
        
        # Шаг 2: Проверка статуса ответа
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        
        # Шаг 3: Проверка содержимого ответа
        response_data = response.json()
        user_data = response_data["user"]
        access_token = response_data["accessToken"]
        
        # Шаг 4: Проверка данных пользователя
        assert 'email' in user_data 
        assert 'name' in user_data 
        assert '@example.com' in user_data['email']
        assert user_data['name'] == "Temp User"
        assert access_token is not None
        assert access_token.startswith('Bearer ')
     
    @allure.title("Тест создания уже существующего пользователя")
    def test_create_existing_user(self):
        response = requests.post(REGISTER_URL, json=EXISTING_USER)
        assert response.status_code == 403, f"Expected status code 403 for existing user, but got {response.status_code}. Response: {response.text}"

        response_data = response.json()
        assert response_data.get('success') is False, f"Expected success: false, but got {response_data.get('success')}"
        assert 'message' in response_data, "Expected 'message' key in response"

        assert response_data['message'] == ERROR_MESSAGES["USER_EXISTS"], \
            f"Message mismatch: Expected '{ERROR_MESSAGES['USER_EXISTS']}', but got '{response_data['message']}'"

    @allure.title("Тест создания пользователя с невалидными данными")
    @pytest.mark.parametrize("test_data,expected_message", INVALID_USER_PAYLOADS)
    def test_create_user_invalid_data(self, test_data, expected_message):
        response = requests.post(REGISTER_URL, json=test_data)
        assert response.status_code == 403, f"Expected status code 403 for invalid data {test_data}, but got {response.status_code}. Response: {response.text}"

        response_data = response.json()
        assert response_data.get('success') is False, f"Expected success: false for invalid data, but got {response_data.get('success')}"
        assert 'message' in response_data, "Expected 'message' key in response for invalid data"

        assert expected_message.lower() in response_data['message'].lower(), \
            f"Message mismatch for data {test_data}: Expected message to contain '{expected_message}', but got '{response_data['message']}'"