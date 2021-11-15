from argparse import Namespace
from textwrap import dedent
import logging

import pytest

from asset import (
	Asset, load_asset_from_file, setup_logging,
	print_asset_revenue, process_cli_arguments,
)

TEST_YAML_FILEPATH = 'task_asset_log.conf.yml'
TEST_ASSET_FILE = dedent("""\
	TSL 400 0.1
""")

@pytest.fixture()
def asset_file(tmpdir):
	asset_file_fio = tmpdir.join("test_asset_file.txt")
	asset_file_fio.write(TEST_ASSET_FILE)
	return asset_file_fio


def test_correct_setup_logging():
	setup_logging(TEST_YAML_FILEPATH)


def test_correct_load_asset_from_file(asset_file):
	asset = load_asset_from_file(asset_file)
	etallon_asset = Asset(name='TSL', capital=400.0, interest=0.1)
	assert asset == etallon_asset


def test_correct_process_cli_argumetns(asset_file, capsys, caplog):
	caplog.set_level("DEBUG")

	periods = [2, 1, 5, 4]
	arguments = Namespace(
			asset_fin=asset_file,
			periods=periods,
	)
	process_cli_arguments(arguments)

	CORRECT_PRINT = [['2:', '84.000'],
					 ['1:', '40.000'],
					 ['5:', '244.204'],
					 ['4:', '185.640']]

	captured = capsys.readouterr().out.split('\n')[:-1]
	captured = [string.strip().split() for string in captured]
	
	assert captured == CORRECT_PRINT
	
	assert any("reading asset file" in message for message in caplog.messages)
	assert any("building asset object" in message for message in caplog.messages)
	assert all(log.levelno < logging.WARNING for log in caplog.records)


def test_warning_if_number_of_periods_upper_then_threshold(asset_file, caplog):
	periods = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	print_asset_revenue(asset_file, periods)
	assert any(log.levelno == logging.WARNING for log in caplog.records)