from helpers import generate_unique_email
import requests

HTTP_METHODS_MAP = {
    'GET': requests.get,
    'POST': requests.post,
    'DELETE': requests.delete,
    'PATCH': requests.patch
}

TEST_USER = {
    "email": "test-order-user@example.com",
    "password": "password123",
    "name": "Test Order User"
}

EXISTING_USER = {
    "email": "existing-user@example.com",
    "password": "password123",
    "name": "Existing User"
}

LOGIN_USER = {
    "email": "test-login@example.com",
    "password": "password123",
    "name": "Test Login User"
}

INVALID_USER_PAYLOADS = [
    ( # Пустой email
        {"email": "", "password": "password123", "name": "Test User"},
        "Email, password and name are required fields"
    ),
    ( # Пустой пароль
        {"email": generate_unique_email(), "password": "", "name": "Test User"},
        "Email, password and name are required fields"
    ),
    ( # Пустое имя
        {"email": generate_unique_email(), "password": "password123", "name": ""},
        "Email, password and name are required fields"
    ),
    ( # Невалидный формат email
        {"email": "invalid-email", "password": "password123", "name": "Test User"},
        "User already exists"
    ),
]

ORDER_TEST_DATA = {
    "VALID_INGREDIENTS": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"],
    "SINGLE_INGREDIENT": ["60d3b41abdacab0026a733c6"],
    "INVALID_INGREDIENTS": ["invalid_hash_12345", "invalid_hash_678901"],
    "EMPTY_INGREDIENTS": []
}

LOGIN_TEST_DATA = {
    "INVALID_CREDENTIALS": {
        "email": "invalid@example.com",
        "password": "wrong_password"
    }
}

ERROR_MESSAGES = {
    "REQUIRED_FIELDS": "Email, password and name are required fields",
    "USER_EXISTS": "User already exists",
    "INVALID_CREDENTIALS": "email or password are incorrect",
    "INGREDIENTS_REQUIRED": "Ingredient ids must be provided",
    "UNAUTHORIZED": "You should be authorised"
}
