import pytest
import requests
from unittest.mock import patch, MagicMock

from task_asset_web_service import (
	app, parse_cbr_currency_base_daily,
	parse_cbr_key_indicators, add_asset, list_asset, 
	get_asset, calculate_revenue_asset, cleanup_asset,
	Asset, URL_CBR_CURRENCY_BASE_DAILY, URL_CBR_KEY_INDICATORS,
)


DUMP_CBR_CURRENCY_BASE_DAILY_PATH = "cbr_currency_base_daily.html"
DUMP_CBR_KEY_INDICATORS = "cbr_key_indicators.html"

CORRECT_RATES_FOR_CURRENCY_DAILY = {
	"AUD": 57.0229,
	"AZN": 44.4127,
	"AMD": 0.144485,
	"BYN": 29.2821,
	"BGN": 46.9816,
	"BRL": 14.6235,
	"HUF": 0.254265,
	"KRW": 00.681688,
	"HKD": 9.73339,
	"DKK": 12.3566,
	"USD": 75.4571,
	"EUR": 91.9822,
	"INR": 1.02294,
	"KZT": 0.179088,
	"CAD": 58.5438,
	"KGS": 0.930621,
	"CNY": 11.5410,
	"MDL": 4.37813,
	"TMT": 21.5900,
	"NOK": 8.66526,
	"PLN": 20.4264,
	"RON": 18.8676,
	"XDR": 108.8099,
	"SGD": 56.5561,
	"TJS": 6.66288,
	"TRY": 9.87607,
	"UZS": 0.00720439,
	"UAH": 2.65297,
	"GBP": 101.1955,
	"CZK": 3.49857,
	"SEK": 9.08618,
	"CHF": 84.8882,
	"ZAR": 5.16900,
	"JPY": 0.729265,
}
CORRECT_RATES_FOR_KEY_INDICATORS = {
	"USD": 75.4571,
	"EUR": 91.9822,
	"Au": 4529.59,
	"Ag": 62.52,
	"Pt": 2459.96,
	"Pd": 5667.14,
}


@pytest.fixture
def client():
	with app.test_client() as client:
		yield client


def test_correct_parse_cbr_currency_base_daily():
	with open(DUMP_CBR_CURRENCY_BASE_DAILY_PATH) as fin:
		rates = parse_cbr_currency_base_daily(fin)
	for key, item in CORRECT_RATES_FOR_CURRENCY_DAILY.items():
		assert rates[key] - item < 1e-8


def test_correct_parse_cbr_key_indicators():
	with open(DUMP_CBR_KEY_INDICATORS) as fin:
		rates = parse_cbr_key_indicators(fin)
	for key, item in CORRECT_RATES_FOR_KEY_INDICATORS.items():
		assert rates[key] - item < 1e-8


def test_cbr_key_indicators_work(client):
	responce = client.get("/cbr/key_indicators")
	responce_text = responce.data.decode(responce.charset)
	assert "USD" in responce_text and "Au" in responce_text
	assert 200 == responce.status_code


def test_cbr_currency_base_daily_work(client):
	responce = client.get("/cbr/daily")
	responce_text = responce.data.decode(responce.charset)
	assert "USD" in responce_text and "CZK" in responce_text
	assert 200 == responce.status_code


@patch("requests.get")
def test_cbr_currency_base_daily_return_503_if_connection_error(mock, client):
	mock.side_effect = requests.exceptions.ConnectionError()
	responce = client.get("/cbr/daily")
	assert 503 == responce.status_code


@patch("requests.get")
def test_cbr_key_indicators_return_503_if_connection_error(mock, client):
	mock.side_effect = requests.exceptions.ConnectionError()
	responce = client.get("/cbr/key_indicators")
	assert 503 == responce.status_code


def test_add_asset_work_correct(client):
	responce = client.get("/api/asset/add/RUS/Rubles/1000/0.1")
	assert "Asset Rubles was successfully added" == responce.data.decode(responce.charset)
	assert 200 == responce.status_code

	client.get("/api/asset/add/EUR/Euro/2000/0.1")
	client.get("/api/asset/add/USD/Dollars/1000/0.2")

	correct_return = [
		["RUS", "Rubles", 1000, 0.1],
		["EUR", "Euro", 2000, 0.1],
		["USD", "Dollars", 1000, 0.2],
	]

	assert app.bank["Rubles"].get_params() == correct_return[0]
	assert app.bank["Euro"].get_params() == correct_return[1]
	assert app.bank["Dollars"].get_params() == correct_return[2]
	assert 3 == len(app.bank)


def test_add_asset_return_403_if_name_repeat(client):
	client.get("/api/asset/add/RUS/Rubles/1000/0.1")
	responce = client.get("/api/asset/add/RUS/Rubles/2000/0.1")
	assert 403 == responce.status_code


def test_list_asset_work_correct(client):
	client.get("/api/asset/cleanup")
	client.get("/api/asset/add/USD/Dollars/5000/0.2")
	client.get("/api/asset/add/EUR/Euro/2000/0.1")
	responce = client.get("/api/asset/list")
	responce_text = responce.data.decode(responce.charset)
	correct_answer = '[["EUR","Euro",2000.0,0.1],["USD","Dollars",5000.0,0.2]]\n'
	assert 200 == responce.status_code
	assert responce_text == correct_answer


def test_get_asset_work_correct(client):
	client.get("/api/asset/cleanup")
	client.get("/api/asset/add/USD/Dollars/5000/0.2")
	client.get("/api/asset/add/EUR/Euro/2000/0.1")
	client.get("/api/asset/add/RUS/Rubles/1000/0.3")
	responce = client.get("/api/asset/get?name=Rubles&name=Dollars")
	responce_text = responce.data.decode(responce.charset)
	correct_answer = '[["RUS","Rubles",1000.0,0.3],["USD","Dollars",5000.0,0.2]]\n'
	assert responce_text == correct_answer
	assert 200 == responce.status_code


def mock_request_get_for_calculate_revenue_asset(url):
	if URL_CBR_KEY_INDICATORS == url:
		with open(DUMP_CBR_KEY_INDICATORS, "rb") as content_fin:
			content = content_fin.read()
			return MagicMock(
				content = content,
				text = content.decode('utf-8'),
			)
	if URL_CBR_CURRENCY_BASE_DAILY == url:
		with open(DUMP_CBR_CURRENCY_BASE_DAILY_PATH, "rb") as content_fin:
			content = content_fin.read()
			return MagicMock(
				content = content,
				text = content.decode('utf-8'),
			)


@patch("requests.get")
def test_calculate_revenue_asset_work_correct(mock, client):
	mock.side_effect = lambda url: mock_request_get_for_calculate_revenue_asset(url)
	client.get("/api/asset/cleanup")
	client.get("/api/asset/add/DKK/DKK/5000/0.2")
	client.get("/api/asset/add/EUR/Euro/2000/0.1")
	client.get("/api/asset/add/RUB/Rubles/1000/0.3")
	
	responce = client.get("/api/asset/calculate_revenue?period=1&period=5")
	responce_text = responce.data.decode(responce.charset)
	correct_answer = '{"1":31053.040000000015,"5":206977.91040400008}\n'
	assert responce_text == correct_answer
	assert 200 == responce.status_code


def test_cleanup_asset_work_correct(client):
	client.get("/api/asset/add/DKK/DKK/5000/0.2")
	client.get("/api/asset/add/EUR/Euro/2000/0.1")
	responce = client.get("/api/asset/cleanup")
	responce_text = responce.data.decode(responce.charset)
	assert "there are no more assets" == responce_text
	assert 200 == responce.status_code
	assert 0 == len(app.bank)


def test_if_page_not_exist(client):
	responce = client.get("/aboba")
	responce_text = responce.data.decode(responce.charset)
	assert 404 == responce.status_code
	assert "This route is not found" == responce_text
