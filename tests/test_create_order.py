import pytest
import requests
import allure
from constants import ORDERS_URL
from data.test_data import ORDER_TEST_DATA, ERROR_MESSAGES

class TestCreateOrder:
     
    @allure.title("Создание заказа с авторизацией") 
    def test_order_with_authorization(self, auth_token):
        ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": ingredients}
        response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})
        assert response.status_code == 200
        
        # Дополнительно проверяем содержимое ответа
        response_body = response.json()
        assert "_id" in response_body["order"] 
        assert "number" in response_body["order"]
        response_ingredients = [item["_id"] for item in response_body["order"]["ingredients"]]
        assert set(response_ingredients) == set(ingredients)
     
    @allure.title("Создание заказа с валидными ингредиентами")
    def test_order_with_valid_ingredients(self, auth_token):
        valid_ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": valid_ingredients}
        response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})
        assert response.status_code == 200
        assert len(response.json()) > 0

        response_body = response.json()
        assert "_id" in response_body["order"]
        assert "number" in response_body["order"]
        response_ingredients = [item["_id"] for item in response_body["order"]["ingredients"]]
        assert set(response_ingredients) == set(valid_ingredients)
 
    @allure.title("Создание заказа без авторизации") 
    def test_order_without_authorization(self, unauthorized_request):     
        valid_ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": valid_ingredients}
        response = unauthorized_request(ORDERS_URL, method='POST')
        assert response.status_code == 401

        response_body = response.json()
        assert "success" in response_body
        assert response_body["success"] == False
        assert "message" in response_body
        assert response_body["message"] == "You should be authorized"


    @allure.title("Создание заказа без ингредиентов") 
    def test_order_without_ingredients(self, auth_token):
        empty_ingredients = ORDER_TEST_DATA["EMPTY_INGREDIENTS"]
        order_payload = {"ingredients": empty_ingredients}
        response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})
        assert response.status_code == 400
        assert ERROR_MESSAGES["INGREDIENTS_REQUIRED"] in response.json()['message']
    

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_with_invalid_ingredients(self, auth_token):
        invalid_ingredients = ORDER_TEST_DATA["INVALID_INGREDIENTS"]
        order_payload = {"ingredients": invalid_ingredients}
        response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})

        # Проверка статуса ответа
        assert response is not None, "Response is None"
        assert response.status_code == 500, f"Expected status code 500, but got {response.status_code}"

        # Проверка содержимого ответа
        assert "Internal Server Error" in response.text, f"Expected 'Internal Server Error' in HTML response, but got '{response.text}'"