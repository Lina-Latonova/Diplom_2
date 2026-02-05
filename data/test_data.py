
VALID_USER_DATA = { 
    "email": "your_real_email@example.com",  
    "password": "your_real_password" 
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
    (
        {"email": "", "password": "password123", "name": "Test User"},
        "required fields"
    ),
    (
        {"email": "test@example.com", "password": "", "name": "Test User"},
        "required fields"
    ),
    (
        {"email": "test@example.com", "password": "password123", "name": ""},
        "required fields"
    ),
    (
        {"email": "invalid-email", "password": "password123", "name": "Test User"},
        "valid email"
    ),
    (
        {"email": "test@example.com", "password": "123", "name": "Test User"},
        "password"
    )
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