from http.client import responses
import requests
import  os
from dotenv import load_dotenv
from requests import Session
import allure
from  core.clients.endpoints import BookingEndpoints
from core.settings.environments import Environment
from core.settings.config import Credentials, Timeouts
from requests.auth import HTTPBasicAuth


load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value:{environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers ={
            "Content-Type": "application/json"
        }

    def get_base_url(self,environment:Environment) -> str:
        if environment== Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment value:{environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping Api Client"):
            url = f"{self.base_url}{BookingEndpoints.PING}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Should be 201, but {response.status_code}, puPuPu..."
            return response.status_code

    def auth(self):
        with allure.step("Getting Autentification"):
            url = f"{self.base_url}{BookingEndpoints.AUTH}"
            payload = {"username": Credentials.USERNAME, "password": Credentials.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

        token = response.json().get("token")

        with allure.step('Updating header with authorization'):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self, booking_id):
        with allure.step(f"Get booking by ID {booking_id}"):
            url = f"{self.base_url}{BookingEndpoints.BOOKING}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Expected status 200, but {response.status_code}"
            return response.json()

    def delete_booking(self, booking_id):  # Объявление метода delete_booking с параметром booking_id
        with allure.step('Deleting booking'):  # Начало шага Allure с описанием "Удаление бронирования"
            url = f"{self.base_url}/{BookingEndpoints.BOOKING}/{booking_id}"  # Формирование URL для удаления конкретного бронирования
            response = self.session.delete(url, auth=HTTPBasicAuth(Credentials.USERNAME,Credentials.PASSWORD))  # Выполнение DELETE-запроса с базовой аутентификацией
            response.raise_for_status()  # Проверка статуса ответа - выброс исключения при ошибке HTTP
        with allure.step('Checking status code'):  # Начало шага Allure с описанием "Проверка статус кода"
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"  # Проверка что статус код равен 201
            return response.status_code == 201  # Возврат результата проверки статус кода (True/False)

    def create_booking(self, booking_data):  # Объявление метода create_booking с параметром booking_data
        with allure.step('Creating booking'):  # Начало шага Allure с описанием "Создание бронирования"
            url = f"{self.base_url}/{BookingEndpoints.BOOKING}"  # Формирование URL для создания бронирования
            response = self.session.post(url,json=booking_data)  # Выполнение POST-запроса с данными бронирования в формате JSON
            response.raise_for_status()  # Проверка статуса ответа - выброс исключения при ошибке HTTP
        with allure.step('Checking status code'):  # Начало шага Allure с описанием "Проверка статус кода"
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"  # Проверка что статус код равен 200
            return response.json()  # Возврат данных ответа в формате JSON

    def get_booking_ids(self, params=None):  # Объявление метода get_booking_ids с необязательным параметром params
        with allure.step('Getting object with bookings'):  # Начало шага Allure с описанием "Получение объекта с бронированиями"
            url = f"{self.base_url}/{BookingEndpoints.BOOKING}"  # Формирование URL для получения списка бронирований
            response = self.session.get(url,params=params)  # Выполнение GET-запроса с возможными параметрами фильтрации
            response.raise_for_status()  # Проверка статуса ответа - выброс исключения при ошибке HTTP
        with allure.step('Checking status code'):  # Начало шага Allure с описанием "Проверка статус кода"
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"  # Проверка что статус код равен 200
            return response.json()  # Возврат данных ответа в формате JSON

    def update_booking (self,booking_data,booking_id):
        with allure.step('Updating booking'):
            url = f"{self.base_url}/{BookingEndpoints.BOOKING}/{booking_id}"
            response = self.session.put(url,json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            return response.json()

    def partial_update_booking (self,booking_id, partial_update_data):
        with allure.step('Partial updating booking'):
            url = f"{self.base_url}/{BookingEndpoints.BOOKING}/{booking_id}"
            response = self.session.patch(url, json=partial_update_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            return response.json()



