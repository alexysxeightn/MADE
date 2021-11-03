"""
Library provides CLI to work with inverted index

use load_documents to load document to build inverted index
use build_inverted_index to build inverted index for provided documents
"""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import Dict, List
from collections import defaultdict
import re
import pickle
import json


class InvertedIndex:
    """
    Class can dump, load inverted index and take answer to query

    use InvertedIndex.query to get result of query
    use InvertedIndex.dump to upload inverted index to disk
    use InvertedIndex.load to load inverted index from disk
    """
    def __init__(self, documents: Dict[str, List[int]]):
        self._data = documents

    def __eq__(self, other: InvertedIndex):
        if self._data is None or other._data is None:
            return False
        self_inverted_index = {k: sorted(v) for k, v in self._data.items()}
        other_inverted_index = {k: sorted(v) for k, v in other._data.items()}
        return self_inverted_index == other_inverted_index

    def query(self, words: List[str]) -> List[int]:
        """
        Return the list of relevant documents for the given query

        function converts all words to lowercase and return
        list of documents ids that contain all this words
        """
        words = [word.lower() for word in words]
        if words[0] not in self._data.keys():
            return []
        answer = set(self._data[words[0]])
        for word in words:
            if word not in self._data.keys():
                return []
            answer = answer & set(self._data[word])
        return list(answer)

    def dump(self, filepath: str, dump_method: str) -> None:
        """
        Dump the Inverted Index into the given path

        function can dump inverted index using pickle or json
        dump_method is 'pickle' or 'json'
        pickle dump in binary file, json dump in ordinary file
        """
        if dump_method == "pickle":
            with open(filepath, 'wb') as file:
                pickle.dump(self._data, file)
        elif dump_method == "json":
            with open(filepath, 'w') as file:
                json.dump(self._data, file)

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        """Load the Inverted Index from given path (so far only json)"""
        with open(filepath, 'r') as file:
            docs = json.load(file)
            return cls(documents=docs)


def load_documents(filepath: str) -> Dict[int, str]:
    """
    Function load dataset from filepath

    function create dict, where key is document id and item is
    document without tab and in lowercase
    """
    documents = dict()

    with open(filepath) as file:
        file_content = file.readlines()

    for line in file_content:
        doc_id, content = line.lower().split("\t", 1)
        doc_id = int(doc_id)
        documents[doc_id] = content.strip()

    return documents


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    """Function return InvertedIndex object, which build on documents"""
    inverted_index = defaultdict(list)

    for key in documents.keys():
        for word in set(re.split(r"\W+", documents[key])):
            inverted_index[word].append(key)

    return InvertedIndex(inverted_index)


def callback_build(arguments):
    """Function for command 'build' is CLI

    function create inverted index on dataset and dump it in output
    dump_method = strategy
    """
    documents = load_documents(arguments.dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(arguments.output, arguments.strategy)


def callback_query(arguments):
    """Function for command 'query' is CLI

    function print result of querys on loa inverted index"""
    inverted_index = InvertedIndex.load(arguments.filepath)
    for query in arguments.query:
        document_ids = inverted_index.query(query)
        print(*document_ids, sep=',')


def setup_parser(parser):
    """Function for developer CLI"""
    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "build", help="build inverted index and save into hard drive",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-s", "--strategy", default="json", choices=['json', 'pickle'],
        help="method to dump inverted index",
    )
    build_parser.add_argument(
        "-d", "--dataset",
        help="path to dataset to load", required=True,
    )
    build_parser.add_argument(
        "-o", "--output",
        help="path to store inverted index", required=True,
    )
    build_parser.set_defaults(callback=callback_build)

    query_parser = subparsers.add_parser(
        "query", help="print result of queries",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser.add_argument(
        "-j", "--json-index", required=True,
        help="path to store inverted index (in .json format)",
        dest="filepath",
    )
    query_parser.add_argument(
        "-q", "--query", help="set of words for query",
        action="append", required=True, nargs="+",
    )
    query_parser.set_defaults(callback=callback_query)


def main():
    parser = ArgumentParser(
        prog="inverted_index",
        description="Inverted Index CLI: tool to build, dump, load and query inverted index",
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
