from http.client import responses
import requests
import  os
from dotenv import load_dotenv
from requests import Session
import allure
from  core.clients.endpoints import BookingEndpoints
from core.settings.environments import Environment
from core.settings.config import Credentials, Timeouts


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
