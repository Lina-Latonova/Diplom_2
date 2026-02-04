import pytest
import requests
import allure
from constants import ORDERS_URL
from data.test_data import ORDER_TEST_DATA, ERROR_MESSAGES
 
class TestCreateOrder:
     
    @allure.title("Создание заказа с авторизацией") 
    def test_create_order_with_authorization(self, auth_token):
        order_data = {
            "ingredients": ORDER_TEST_DATA["VALID_INGREDIENTS"]
        }

        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': auth_token},
            json=order_data
        )

        # Проверяем статус-код ответа сервера
        assert response.status_code == 200
        # Проверяем наличие успешного результата
        assert response.json()['success'] is True
        # Проверяем структуру ответа
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']
     
    @allure.title("Создание заказа с ингредиентами") 
    def test_create_order_with_ingredients(self, auth_token): 
        order_data = {
            "ingredients": ORDER_TEST_DATA["VALID_INGREDIENTS"]
        }
         
        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': auth_token},
            json=order_data
        )
         
        assert response.status_code == 200 
        assert response.json()['success'] == True
        assert 'order' in response.json()
        assert 'number' in response.json()['order']
        assert 'name' in response.json()
 
    @allure.title("Создание заказа без авторизации") 
    def test_order_without_authorization(self): 
        order_data = {
            "ingredients": ORDER_TEST_DATA["SINGLE_INGREDIENT"]
        }
         
        response = requests.post(ORDERS_URL, json=order_data)
         
        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == ERROR_MESSAGES["UNAUTHORIZED"]
     
    @allure.title("Создание заказа без ингредиентов") 
    def test_order_without_ingredients(self, auth_token): 
        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': auth_token},
            json={"ingredients": ORDER_TEST_DATA["EMPTY_INGREDIENTS"]}
        )
         
        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == ERROR_MESSAGES["INGREDIENTS_REQUIRED"]
     
    @allure.title("Создание заказа с невалидным хешем ингредиента") 
    def test_order_with_invalid_ingredient_hash(self, auth_token):
        order_data = {
            "ingredients": ORDER_TEST_DATA["INVALID_INGREDIENTS"]
        }

        response = requests.post(
            ORDERS_URL,
            headers={'Authorization': auth_token},
            json=order_data
        )

        # Проверяем статус-код ответа сервера
        assert response.status_code == 500

        # Так как ответ содержит HTML с сообщением об ошибке, проверим его прямо текстом
        error_text = response.text.strip()
        assert "<pre>Internal Server Error</pre>" in error_text