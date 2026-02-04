import pytest
import requests
import uuid
import logging
from data.test_data import TEST_USER, EXISTING_USER, LOGIN_USER
from constants import REGISTER_URL, LOGIN_URL, DELETE_URL

logger = logging.getLogger(__name__)

# Фикстура для подготовки общих тестовых данных
@pytest.fixture(scope="session", autouse=True)
def prepare_test_data():
    # Регистрация основных пользователей вне тестов
    for user in [TEST_USER, EXISTING_USER, LOGIN_USER]:
        try:
            response = requests.post(REGISTER_URL, json=user)
            
            if response.status_code == 403:
                logger.info(f"Пользователь уже существует: {user['email']}")
            elif response.status_code == 200:
                logger.info(f"Создан пользователь: {user['email']}")
            else:
                logger.error(f"Неожиданный статус-код: {response.status_code}, Response Body: {response.text}")
        except requests.RequestException as e:
            logger.exception(f"Ошибка при создании пользователя: {e}")

# Фикстура для получения токена авторизации
@pytest.fixture
def auth_token():
    login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
    response = requests.post(LOGIN_URL, json=login_data)
    
    if response.status_code == 200:
        return response.json()["accessToken"]
    else:
        pytest.skip("Не удалось авторизоваться.")

# Новая фикстура для создания и удаления временного пользователя в каждом отдельном тесте
@pytest.fixture
def create_temp_user():
    """
    Регистрирует временного пользователя и удаляет его после завершения теста.
    Возвращает кортеж (user_data, access_token).
    """
    unique_email = f"temp_user_{uuid.uuid4()}@example.com"
    password = "temp_password"
    name = "Temp User"
    
    register_response = requests.post(REGISTER_URL, json={
        "email": unique_email,
        "password": password,
        "name": name
    })
    
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
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if delete_response.status_code != 200:
        logger.warning(f"Не удалось удалить временный аккаунт: {delete_response.text}. Возможно, произошла ошибка.")