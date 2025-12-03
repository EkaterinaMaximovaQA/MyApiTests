import  allure
import  pytest
import requests


@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):  # Объявляем тест, который принимает фикстуру api_client
    status_code = api_client.ping()  # Вызываем метод ping() клиента, получаем статус-код
    assert status_code == 201, f"Expected status 201 but got {status_code}"


@allure.feature('Test Ping')
@allure.story('Test server unavailable')
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))  # Мокаем  get у сессии, чтобы он бросал side_effect
    with pytest.raises(Exception, match="Server unavailable"):  # Проверяем что код внутри блока вызывает исключение
        api_client.ping()  # Вызываем метод ping(), который должен упасть с исключением

@allure.feature('Test Ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):  # Тест принимает клиент API и мокер для подмены реальных вызовов
    mock_response = mocker.Mock()  # Создаем мок-объект, который будет имитировать ответ сервера
    mock_response.status_code = 405  # мокаем статус 405 (Method Not Allowed)
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)  # Подменяем реальный HTTP GET запрос на наш мок с ответом 405
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):  # Ожидаем, что код внутри вызовет AssertionError с таким текстом
        api_client.ping()  # Вызываем метод ping(), который должен упасть с AssertionError потому что ожидает 201, а получит 405

@allure.feature('Test Ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()

@allure.feature('Test Ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)  # Подменяем реальный HTTP GET запрос так, чтобы он всегда выбрасывал исключение Timeout
    with pytest.raises(requests.Timeout):  # Проверяем, что код внутри этого блока выбросит исключение типа Timeout
        api_client.ping()  # Вызываем метод ping(), который должен упасть с исключением Timeout из-за нашей подмены