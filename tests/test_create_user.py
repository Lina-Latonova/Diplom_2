import pytest
import requests
import allure
from constants import REGISTER_URL
from data.test_data import EXISTING_USER, INVALID_USER_PAYLOADS  

@pytest.mark.usefixtures("create_temp_user")
class TestCreateUser:
     
    @allure.title("Тест создания уникального пользователя") 
    def test_create_unique_user(self, create_temp_user):
        """Тест создания уникального пользователя""" 
        user_data, access_token = create_temp_user
        
        assert 'email' in user_data 
        assert 'name' in user_data 
        #assert '_id' in user_data
        assert '@example.com' in user_data['email']
        assert user_data['name'] == "Temp User"
        assert access_token is not None
        assert access_token.startswith('Bearer ')
     
    @allure.title("Тест создания уже существующего пользователя") 
    def test_create_existing_user(self): 
        """Тест создания уже существующего пользователя"""
        response = requests.post(REGISTER_URL, json=EXISTING_USER) 
         
        assert response.status_code == 403 
        assert response.json()['success'] is False 
        assert 'message' in response.json() 
        assert response.json()['message'] == 'User already exists'
 
    @allure.title("Тест создания пользователя с невалидными данными") 
    @pytest.mark.parametrize("test_data,expected_message", INVALID_USER_PAYLOADS)  
    def test_create_user_invalid_data(self, test_data, expected_message): 
        """Параметризованный тест создания пользователя с невалидными данными""" 
        response = requests.post(REGISTER_URL, json=test_data) 
         
        assert response.status_code == 403 
        assert response.json()['success'] is False 
        assert 'message' in response.json() 
        assert expected_message.lower() in response.json()['message'].lower()