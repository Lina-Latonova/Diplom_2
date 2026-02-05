# constants.py
BASE_URL = 'https://stellarburgers.education-services.ru/'

# Auth endpoints
REGISTER_URL = f'{BASE_URL}/api/auth/register'
LOGIN_URL = f'{BASE_URL}/api/auth/login'
LOGOUT_URL = f'{BASE_URL}/api/auth/logout'
DELETE_URL = f'{BASE_URL}/api/auth/user'
TOKEN_URL = f'{BASE_URL}/api/auth/token'

# Orders endpoints
ORDERS_URL = f'{BASE_URL}/api/orders'
ALL_ORDERS_URL = f'{BASE_URL}/api/orders/all'

# Ingredients endpoints  
INGREDIENTS_URL = f'{BASE_URL}/api/ingredients'

# Password reset endpoints
PASSWORD_RESET_URL = f'{BASE_URL}/api/password-reset'
PASSWORD_RESET_RESET_URL = f'{BASE_URL}/api/password-reset/reset'