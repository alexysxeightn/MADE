import pytest
import requests
import json
from unittest.mock import patch

from task_web_service_log import app, parse_wiki_search


DUMP_WIKIPEDIA_FILEPATH = "wikipedia_dump.html"


@pytest.fixture
def client():
	with app.test_client() as client:
		yield client


def test_parse_wiki_search_work_correct():
	with open(DUMP_WIKIPEDIA_FILEPATH) as fin:
		article_count = parse_wiki_search(fin)
	assert 2491 == article_count


def test_search_on_wiki_work_correct(client):
	responce = client.get("/api/search?query=python+network")
	responce_json = json.loads(responce.data.decode(responce.charset))
	assert 1.0 == responce_json['version']
	assert responce_json['article_count'] != 0

	responce = client.get("/api/search?query=gblskbgalsjbgjsdal")
	responce_json = json.loads(responce.data.decode(responce.charset))
	assert 1.0 == responce_json['version']
	assert responce_json['article_count'] == 0


def test_if_page_not_exist(client):
	responce = client.get("/aboba")
	responce_text = responce.data.decode(responce.charset)
	assert 404 == responce.status_code
	assert "This route is not found" == responce_text


@patch("requests.get")
def test_search_on_wiki_return_503_if_connection_error(mock, client):
	mock.side_effect = requests.exceptions.ConnectionError()
	responce = client.get("/api/search?query=python+network")
	assert 503 == responce.status_code
