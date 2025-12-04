import  allure
import  pytest
import requests
from faker import Faker


@allure.feature('Create Booking')
@allure.story('Create booking with valid data')
def test_create_booking_success(api_client_auth, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response_data = api_client_auth.create_booking(booking_data)
    assert "bookingid" in response_data, "В ответе нет bookingid"
    assert "booking" in response_data, "В ответе нет booking"
    booking_in_response = response_data["booking"] #Проверяем что данные вернулись те же
    assert booking_in_response["firstname"] == booking_data["firstname"], "Имя не совпадает"
    assert booking_in_response["lastname"] == booking_data["lastname"], "Фамилия не совпадает"
    assert booking_in_response["totalprice"] == booking_data["totalprice"], "Цена не совпадает"
    assert booking_in_response["depositpaid"] == booking_data["depositpaid"], "Депозит не совпадает"
    assert booking_in_response["additionalneeds"] == booking_data["additionalneeds"], "Доп. нужды не совпадают"
    assert booking_in_response["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert booking_in_response["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    booking_id = response_data["bookingid"]
    assert isinstance(booking_id, int), "bookingid должен быть числом"
    assert booking_id > 0, "bookingid должен быть больше 0"

@allure.feature('Create Booking')
@allure.story('Create booking with missing firstname')
def test_create_booking_missing_firstname(api_client_auth):
    invalid_data= {
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }
    with pytest.raises(requests.exceptions.HTTPError):
        api_client_auth.create_booking(invalid_data)


@allure.feature('Create Booking')
@allure.story('Сreate booking with number instead of boolean for depositpaid')
def test_create_booking_number_instead_of_boolean(api_client_auth):
    invalid_data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 100,
        "depositpaid": 1,
        "bookingdates": {
            "checkin": "2018-01-01",

        },
        "additionalneeds": "Breakfast"
    }
    with pytest.raises(requests.exceptions.HTTPError):
        api_client_auth.create_booking(invalid_data)










