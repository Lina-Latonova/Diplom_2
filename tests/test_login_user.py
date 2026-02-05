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
         
        login_response = requests.post(LOGIN_URL, json=login_data)
         
        assert login_response.status_code == 200 
        assert login_response.json()['success'] is True 
        assert 'accessToken' in login_response.json() 
        assert 'refreshToken' in login_response.json() 
        assert 'user' in login_response.json() 
         
        user_data = login_response.json()['user']
        assert user_data['email'] == LOGIN_USER["email"]
        assert user_data['name'] == LOGIN_USER["name"]
     
    @allure.title("Тест входа с неверными учетными данными") 
    def test_login_invalid_credentials(self): 
        invalid_response = requests.post(LOGIN_URL, json=LOGIN_TEST_DATA["INVALID_CREDENTIALS"])
         
        assert invalid_response.status_code == 401 
        assert invalid_response.json()['success'] is False 
        assert invalid_response.json()['message'] == ERROR_MESSAGES["INVALID_CREDENTIALS"]