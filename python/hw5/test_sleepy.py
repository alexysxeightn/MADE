from unittest.mock import patch
from sleepy import sleep_add, sleep_multiply, deepest_sleep_function


@patch("sleepy.sleep")
def test_sleep_add_work_correct(mock_sleep_add):
	z = sleep_add(2, 2)
	mock_sleep_add.assert_called_once_with(3)
	assert 4 == z


@patch("time.sleep")
def test_sleep_multiply_work_correct(mock_sleep_multiply):
	z = sleep_multiply(2, 2)
	mock_sleep_multiply.assert_called_once_with(5)
	assert 4 == z


@patch("time.sleep")
@patch("sleepy.sleep")
def test_can_mock_all_sleep(mock_sleep_add, mock_sleep_multiply):
	outcome = deepest_sleep_function(1, 2)
	assert 5 == outcome
	mock_sleep_add.assert_called_once_with(3)
	mock_sleep_multiply.assert_called_once_with(5)