import  allure
import  pytest
import requests
from faker import Faker


@allure.feature('Create Booking')
@allure.story('Create booking with valid data')
def test_create_booking_success(api_client_no_auth, generate_random_booking_data, mocker):
    booking_data = generate_random_booking_data
    faker = Faker()
    random_booking_id = faker.random_int(min=1, max=99999)
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "bookingid": random_booking_id,
        "booking": booking_data
    }
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    response = api_client_no_auth.create_booking(booking_data)
    assert response.status_code == 200
    assert "bookingid" in response.json()
    assert response.json()["bookingid"] == random_booking_id

@allure.feature('Create Booking')
@allure.story('Create booking without required field: firstname')
def test_create_booking_without_firstname(api_client_no_auth, mocker):
    invalid_data = {
        "lastname": "Doe",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-02"
        }
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    response = api_client_no_auth.create_booking(invalid_data)
    assert response.status_code == 400

@allure.feature('Create Booking')
@allure.story('Create booking with wrong data type: string instead of int for price')
def test_create_booking_string_price(api_client_no_auth, mocker):
    invalid_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": "ван хагрит раблс",
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-02"
        }
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    response = api_client_no_auth.create_booking(invalid_data)
    assert response.status_code == 400

@allure.feature('Create Booking')
@allure.story('Create booking with invalid dates: checkout before checkin')
def test_create_booking_invalid_dates(api_client_no_auth, mocker):
    invalid_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-12-31",
            "checkout": "2000-01-01"
        }
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    response = api_client_no_auth.create_booking(invalid_data)
    assert response.status_code == 400

@allure.feature('Create Booking')
@allure.story('Unprocessable Entity')
def test_create_booking_unprocessable_entity(api_client_no_auth, mocker):
    invalid_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": -45,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-12-31",
            "checkout": "2025-01-01"
        }
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 422
    mock_response.json.return_value = {
        "errors": {
            "totalprice": ["Must be positive number"]
        }
    }
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    response = api_client_no_auth.create_booking(invalid_data)
    assert response.status_code == 400

@allure.feature('Create Booking')
@allure.story('Internal Server Error')
def test_create_booking_internal_server_error(api_client_no_auth, generate_random_booking_data, mocker):
    valid_data = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.reason = "Internal Server Error"
    mock_response.raise_for_status.side_effect = Exception("Server error!")
    mocker.patch.object(api_client_no_auth.session, 'post', return_value=mock_response)
    assert mock_response.status_code == 500
    assert mock_response.reason == "Internal Server Error"



