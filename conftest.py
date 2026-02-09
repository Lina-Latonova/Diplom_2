import pytest
import requests
import uuid
import logging
from data.test_data import TEST_USER, EXISTING_USER
from constants import REGISTER_URL, LOGIN_URL, DELETE_URL

logger = logging.getLogger(__name__)

# Фикстура для получения токена авторизации
@pytest.fixture
def auth_token():
    login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
    response = requests.post(LOGIN_URL, json=login_data)
    
    if response.status_code == 200:
        return response.json()["accessToken"]
    else:
        pytest.skip("Не удалось авторизоваться.")

# Фикстура для создания и удаления временного пользователя в каждом отдельном тесте
@pytest.fixture
def temp_user():
    unique_email = f"temp_user_{uuid.uuid4()}@example.com"
    password = "temp_password"
    name = "Temp User"
    
    register_response = requests.post(REGISTER_URL, json={
        "email": unique_email,
        "password": password,
        "name": name})
    
    if register_response.status_code != 200:
        raise Exception(f"Не удалось создать временный аккаунт: {register_response.text}")
    
    response_data = register_response.json()
    user_data = response_data["user"]
    access_token = response_data["accessToken"]
    
    logger.info(f"Создан временный пользователь: {user_data['email']}")
    
    yield user_data, access_token
    
    # Удаление пользователя после завершения теста
    delete_response = requests.delete(
        DELETE_URL,
        headers={"Authorization": f"Bearer {access_token}"})
    
    if delete_response.status_code != 200:
        logger.warning(f"Не удалось удалить временный аккаунт: {delete_response.text}. Возможно, произошла ошибка.")

# Дополнительная фикстура для случая с заведомо существующим пользователем
@pytest.fixture
def existing_user():
    return EXISTING_USER

# Фикстура для отправки запросов без авторизации
@pytest.fixture
def unauthorized_request():
    def send_unauthorized_request(url, method='GET'):
        methods_map = {'GET': requests.get, 'POST': requests.post, 'DELETE': requests.delete}
        request_method = methods_map.get(method.upper())
        if not request_method:
            raise ValueError(f"Неподдерживаемый HTTP-метод: {method}")
        return request_method(url)
    return send_unauthorized_request