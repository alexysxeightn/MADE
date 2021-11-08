import sys
from io import TextIOWrapper, BytesIO
from unittest.mock import patch
from argparse import Namespace

from task_Khmelev_Alexey_inverted_index import (
	process_queries, process_build, InvertedIndex, EncodedFileType,
	callback_query, callback_build,
)

TEST_INVERTED_INDEX_STORE_PATH_STRUCT = './struct_inverted.index'
TEST_INVERTED_INDEX_STORE_PATH_JSON = './json_inverted.index'
TEST_QUERY_STORE_PATH_UTF8 = './queries_utf8.txt'
TEST_QUERY_STORE_PATH_CP1251 = './queries_cp1251.txt'
TEST_DATASET_STORE_PATH = './dataset.txt'
TEST_OUTPUT_STORE_PATH = './test_inverted.index'

TEST_CORRECT_ANSWER_ON_QUERIES = [['12', '13'],
				  ['123', '37'],
				  ['12'],
				  [''],
				  [''],
				  ['']]

def test_process_queries_can_process_all_queries_from_file_utf8_struct(capsys):
	with open(TEST_QUERY_STORE_PATH_UTF8) as queries_fin:
		process_queries(
			inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_STRUCT,
			query_file=queries_fin,
		)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_queries_can_process_all_queries_from_file_cp1251_struct(capsys):
	with open(TEST_QUERY_STORE_PATH_CP1251, encoding='cp1251') as queries_fin:
		arguments = Namespace(
			inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_STRUCT,
			query_file=queries_fin,
			strategy='struct',
			query=None,
		)
		callback_query(arguments)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_queries_can_process_all_queries_struct(capsys):
	queries = ['строчка', 'A_word', 'тестовая строчка', 'белибирда', 'A_word тестовая']
	process_queries(
		inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_STRUCT,
		queries=queries,
	)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_queries_can_process_all_queries_from_file_utf8_json(capsys):
	with open(TEST_QUERY_STORE_PATH_UTF8) as queries_fin:
		process_queries(
			inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_JSON,
			query_file=queries_fin,
			strategy='json',
		)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_queries_can_process_all_queries_from_file_cp1251_json(capsys):
	with open(TEST_QUERY_STORE_PATH_CP1251, encoding='cp1251') as queries_fin:
		process_queries(
			inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_JSON,
			query_file=queries_fin,
			strategy='json',
		)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_queries_can_process_all_queries_json(capsys):
	queries = ['строчка', 'A_word', 'тестовая строчка', 'белибирда', 'A_word тестовая']
	process_queries(
		inverted_index_filepath=TEST_INVERTED_INDEX_STORE_PATH_JSON,
		queries=queries,
		strategy='json',
	)
	captured = capsys.readouterr().out.split('\n')
	for i, correct_query in enumerate(TEST_CORRECT_ANSWER_ON_QUERIES):
		assert sorted(captured[i].split(',')) == correct_query


def test_process_build_can_build_inverted_index_json():
	process_build(
		dataset=TEST_DATASET_STORE_PATH,
		strategy='json',
		output=TEST_OUTPUT_STORE_PATH,
	)
	inverted_index_process_build = InvertedIndex.load(TEST_OUTPUT_STORE_PATH, strategy="json")
	inverted_index_etalon = InvertedIndex.load(TEST_INVERTED_INDEX_STORE_PATH_STRUCT, strategy="struct")
	assert inverted_index_process_build == inverted_index_etalon


def test_process_build_can_build_inverted_index_struct():
	arguments = Namespace(
		dataset=TEST_DATASET_STORE_PATH,
		strategy='struct',
		output=TEST_OUTPUT_STORE_PATH,
	)
	callback_build(arguments)
	inverted_index_process_build = InvertedIndex.load(TEST_OUTPUT_STORE_PATH, strategy="struct")
	inverted_index_etalon = InvertedIndex.load(TEST_INVERTED_INDEX_STORE_PATH_STRUCT, strategy="struct")
	assert inverted_index_process_build == inverted_index_etalon


def test_EncodedFileType_work_correct_r_utf8():
	with open(TEST_QUERY_STORE_PATH_UTF8, 'r') as stdin:
		sys.stdin = stdin
		EFT = EncodedFileType('r', encoding='utf-8')
		EFT_ = EFT('-')
		assert str(type(EFT_)) == '<class \'_io.TextIOWrapper\'>'
		assert EFT_.encoding == 'utf-8'
		assert EFT._mode == 'r'
