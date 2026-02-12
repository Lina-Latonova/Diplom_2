import pytest
import requests
import allure
from constants import ORDERS_URL
from data.test_data import ORDER_TEST_DATA, ERROR_MESSAGES, HTTP_METHODS_MAP

class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_order_with_authorization(self, auth_token):
        ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": ingredients}

        with allure.step("Отправка POST-запроса для создания заказа с токеном"):
            response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})

        assert response.status_code == 200

        with allure.step("Проверка тела ответа: наличие _id, number и совпадение ингредиентов"):
            response_body = response.json()
            assert "_id" in response_body["order"]
            assert "number" in response_body["order"]
            response_ingredients = [item["_id"] for item in response_body["order"]["ingredients"]]
            assert set(response_ingredients) == set(ingredients)


    @allure.title("Создание заказа с валидными ингредиентами")
    def test_order_with_valid_ingredients(self, auth_token):
        valid_ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": valid_ingredients}

        with allure.step("Отправка POST-запроса для создания заказа с валидными ингредиентами"):
            response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})

        assert response.status_code == 200
        assert len(response.json()) > 0

        with allure.step("Проверка тела ответа: наличие _id, number и совпадение ингредиентов"):
            response_body = response.json()
            assert "_id" in response_body["order"]
            assert "number" in response_body["order"]
            response_ingredients = [item["_id"] for item in response_body["order"]["ingredients"]]
            assert set(response_ingredients) == set(valid_ingredients)


    @allure.title("Создание заказа без авторизации")
    def test_order_without_authorization(self):
        valid_ingredients = ORDER_TEST_DATA["VALID_INGREDIENTS"]
        order_payload = {"ingredients": valid_ingredients}
        url = ORDERS_URL
        method = 'POST'
        request_method = HTTP_METHODS_MAP[method.upper()]

        with allure.step(f"Отправка {method}-запроса для создания заказа без авторизации"):
            response = request_method(url, json=order_payload)

        assert response.status_code == 401

        with allure.step("Проверка тела ответа: ошибка авторизации"):
            response_body = response.json()
            assert "success" in response_body
            assert response_body["success"] == False
            assert "message" in response_body
            assert response_body["message"] == "You should be authorized"


    @allure.title("Создание заказа без ингредиентов")
    def test_order_without_ingredients(self, auth_token):
        empty_ingredients = ORDER_TEST_DATA["EMPTY_INGREDIENTS"]
        order_payload = {"ingredients": empty_ingredients}

        with allure.step("Отправка POST-запроса для создания заказа без ингредиентов"):
            response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})

        assert response.status_code == 400

        with allure.step("Проверка тела ответа: сообщение об обязательных ингредиентах"):
            assert ERROR_MESSAGES["INGREDIENTS_REQUIRED"] in response.json()['message']


    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_with_invalid_ingredients(self, auth_token):
        invalid_ingredients = ORDER_TEST_DATA["INVALID_INGREDIENTS"]
        order_payload = {"ingredients": invalid_ingredients}

        with allure.step("Отправка POST-запроса для создания заказа с неверным хешем ингредиентов"):
            response = requests.post(ORDERS_URL, json=order_payload, headers={"Authorization": auth_token})

        assert response is not None, "Response is None"
        assert response.status_code == 500, f"Expected status code 500, but got {response.status_code}"

        with allure.step("Проверка текста ответа: наличие 'Internal Server Error'"):
            assert "Internal Server Error" in response.text, f"Expected 'Internal Server Error' in HTML response, but got '{response.text}'"
