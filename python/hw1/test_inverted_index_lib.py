from textwrap import dedent

import pytest

from task_inverted_index_lib import load_documents, build_inverted_index, InvertedIndex


DATASET_TINY_STR = dedent("""\
	123	some words A_word and nothing
	2 	some word B_word in this dataset
	5	famous_phrases to be or not to be
	37	all words such as A_word and B_word are here
""")

@pytest.fixture()
def tiny_dataset_fio(tmpdir):
	dataset_fio = tmpdir.join("dataset.txt")
	dataset_fio.write(DATASET_TINY_STR)
	return dataset_fio

def test_can_load_documents(tiny_dataset_fio):
	documents = load_documents(tiny_dataset_fio)
	etalon_documents = {
		123: "some words a_word and nothing",
		2: "some word b_word in this dataset",
		5: "famous_phrases to be or not to be",
		37: "all words such as a_word and b_word are here",
	}
	assert etalon_documents == documents, (
		"load documents incorrectly loaded dataset"
	)

@pytest.mark.parametrize(
	"query, etalon_answer",
	[
		pytest.param(["A_word"], [123, 37], id = "A_word"),
		pytest.param(["B_word"], [2, 37], id = "B_word"),
		pytest.param(["A_word", "B_word"], [37], id = "both words"),
		pytest.param(["word_does_not_exist"], [], id = "word does not exist"),
	],
)

def test_query_inverted_index_intersect_results(tiny_dataset_fio, query, etalon_answer):
	documents = load_documents(tiny_dataset_fio)
	tiny_inverted_index = build_inverted_index(documents)
	answer = tiny_inverted_index.query(query)	
	assert sorted(answer) == sorted(etalon_answer), (
		f"Expected answer is {etalon_answer}, but you got {answer}"
	)

def test_can_build_and_query_inverted_index(tiny_dataset_fio):
	tiny_inverted_index = build_inverted_index(load_documents(tiny_dataset_fio))
	doc_ids = tiny_inverted_index.query(["some"])
	assert isinstance(doc_ids, list), "inverted index query should return list"

@pytest.fixture
def tiny_dataset_inverted_index(tiny_dataset_fio):
	return build_inverted_index(load_documents(tiny_dataset_fio))

def test_can_dump_and_load_inverted_index(tmpdir, tiny_dataset_inverted_index):
	index_fio = tmpdir.join("index.dump")
	tiny_dataset_inverted_index.dump(index_fio)
	loaded_tiny_dataset_inverted_index = InvertedIndex.load(index_fio)
	assert tiny_dataset_inverted_index == loaded_tiny_dataset_inverted_index, (
		"load should return the same inverted index"
	)
