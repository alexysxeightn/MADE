import pytest
import requests
from argparse import Namespace
from unittest.mock import patch

from task_Khmelev_Alexey_web_spy import (
	URL_GITLAB, process_for_gitlab, print_result_gitlab,
)

GITLAB_HTML_DUMP_FILEPATH = 'gitlab_features.html'
GITLAB_EXPECTED_HTML_DUMP_FILEPATH = 'gitlab_features_expected.html'
DEFAULT_STATUS_CODE = 200


@patch("requests.get")
def process_for_gitlab_expected_html_dump(mock_requests_get):
	with open(GITLAB_EXPECTED_HTML_DUMP_FILEPATH, "r") as fin:
		text = fin.read()
		mock_requests_get.return_value = Namespace(
			text=text,
			status_code=DEFAULT_STATUS_CODE,
		)
	return process_for_gitlab(URL_GITLAB)


@pytest.mark.integration_test
def test_gitlab_request_is_successful():
	response = requests.get(URL_GITLAB)
	assert bool(response)


@pytest.mark.integration_test
def test_with_internet_process_for_gitlab_return_not_zero_values():
	response = requests.get(URL_GITLAB)
	num_free_products, num_enterprise_products = process_for_gitlab(URL_GITLAB)
	assert num_free_products > 0
	assert num_enterprise_products > 0


@pytest.mark.integration_test
def test_with_internet_correct_output(capsys):
	response = requests.get(URL_GITLAB)
	print_result_gitlab()
	captured = capsys.readouterr().out.split('\n')
	assert 'free products: ' in captured[0]
	assert 'enterprise products: ' in captured[1]


@pytest.mark.integration_test
def test_with_internet_process_for_gitlab_return_correct_value():
	num_free_products_expected, num_enterprise_products_expected = process_for_gitlab_expected_html_dump()
	num_free_products, num_enterprise_products = process_for_gitlab(URL_GITLAB)
	assert num_enterprise_products == num_enterprise_products_expected and num_free_products == num_free_products_expected, (
		f"expected free product count is {num_free_products_expected}, while you calculated {num_free_products};"
		f" expected enterprise product count is {num_enterprise_products_expected}, while you calculated {num_enterprise_products}"
	)


@pytest.mark.slow
@patch("requests.get")
def test_without_internet_process_for_gitlab_return_not_zero_values(mock_requests_get):
	with open(GITLAB_HTML_DUMP_FILEPATH, "r") as fin:
		text = fin.read()
		mock_requests_get.return_value = Namespace(
			text=text,
			status_code=DEFAULT_STATUS_CODE,
		)
	response = requests.get(URL_GITLAB)
	num_free_products, num_enterprise_products = process_for_gitlab(URL_GITLAB)
	assert num_free_products > 0
	assert num_enterprise_products > 0


@pytest.mark.slow
@patch("requests.get")
def test_without_internet_correct_output(mock_requests_get, capsys):
	with open(GITLAB_HTML_DUMP_FILEPATH, "r") as fin:
		text = fin.read()
		mock_requests_get.return_value = Namespace(
			text=text,
			status_code=DEFAULT_STATUS_CODE,
		)
	response = requests.get(URL_GITLAB)
	print_result_gitlab()
	captured = capsys.readouterr().out.split('\n')
	assert 'free products: ' in captured[0]
	assert 'enterprise products: ' in captured[1]