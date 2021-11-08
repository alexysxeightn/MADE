"""
Library provides CLI to work with inverted index

use load_documents to load document to build inverted index
use build_inverted_index to build inverted index for provided documents
"""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from typing import Dict, List
from collections import defaultdict
from io import TextIOWrapper
import re
import json
import sys
import struct


class EncodedFileType(FileType):
    """
    Modified class FileType for work with encoding
    """
    def __call__(self, string):
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            if 'r' in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
                return stdin
            if 'w' in self._mode:
                stdout = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
                return stdout
            msg = 'argument "-" with mode %r' % self._mode
            raise ValueError(msg)
        # all other arguments are used as file names
        try:
            return open(string, self._mode, self._bufsize, self._encoding,
                        self._errors)
        except OSError as e:
            args = {'filename': string, 'error': e}
            message = "can't open '%(filename)s': %(error)s"
            raise ArgumentTypeError(message % args)


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
        result = (self_inverted_index == other_inverted_index)
        return result

    def query(self, words: List[str]) -> List[int]:
        """
        Return the list of relevant documents for the given query

        function converts all words to lowercase and return
        list of documents ids that contain all this words
        """
        words = [word.lower() for word in words]
        if words[0] not in self._data.keys():
            return []
        answer = self._data[words[0]]
        answer = set(answer)
        for word in words:
            if word not in self._data.keys():
                return []
            new_words_for_answer = self._data[word]
            new_words_for_answer = set(new_words_for_answer)
            answer = answer & new_words_for_answer
        answer = list(answer)
        return answer

    def dump(self, filepath: str, strategy: str) -> None:
        """
        Dump the Inverted Index into the given path

        function can dump inverted index using struct or json
        dump_method is 'struct' or 'json'
        struct dump in binary file, json dump in ordinary file
        """
        if strategy == "struct":
            array_of_pairs = []
            array_of_doc_ids = []
            with open(filepath, 'wb') as file:
                for word, doc_ids in self._data.items():
                    len_doc_ids = len(doc_ids)
                    array_of_pairs.append((word, len_doc_ids))
                    array_of_doc_ids += doc_ids

                header = json.dumps(array_of_pairs, ensure_ascii=False)
                header = header.encode('utf8')
                len_header = len(header)
                meta = struct.pack('!I', len_header)
                file.write(meta)

                header = struct.pack('!{}s'.format(len_header), header)
                file.write(header)

                len_array_of_doc_ids = len(array_of_doc_ids)
                body = struct.pack('!{}H'.format(len_array_of_doc_ids), *array_of_doc_ids)
                file.write(body)
        elif strategy == "json":
            with open(filepath, 'w') as file:
                json.dump(self._data, file)

    @classmethod
    def load(cls, filepath: str, strategy: str) -> InvertedIndex:
        """Load the Inverted Index from given path"""
        if strategy == "struct":
            with open(filepath, 'rb') as file:
                binary_data = file.read()

            unsigned_int_size = struct.calcsize('!I')
            char_size = struct.calcsize('!s')
            unsigned_short_size = struct.calcsize('!H')

            meta = binary_data[:unsigned_int_size]
            binary_data = binary_data[unsigned_int_size:]
            meta, = struct.unpack("!I", meta)

            separator = meta * char_size
            header = binary_data[:separator]
            binary_data = binary_data[separator:]
            len_header = len(header)
            len_header //= char_size
            header, = struct.unpack("!{}s".format(len_header), header)
            header = header.decode('utf8')
            header = json.loads(header)

            docs = defaultdict(list)

            for word, len_doc_ids in header:
                separator = len_doc_ids * unsigned_short_size
                doc_ids = binary_data[:separator]
                binary_data = binary_data[separator:]
                doc_ids = struct.unpack("!{}H".format(len_doc_ids), doc_ids)
                docs[word] = doc_ids
        elif strategy == "json":
            with open(filepath, 'r') as file:
                docs = json.load(file)

        load_inverted_index = cls(documents=docs)

        return load_inverted_index


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
        words = set(re.split(r"\W+", documents[key]))
        for word in words:
            inverted_index[word].append(key)

    inverted_index = InvertedIndex(inverted_index)

    return inverted_index


def callback_build(arguments):
    """ Wrapper over process_build function """
    return process_build(arguments.dataset, arguments.strategy, arguments.output)


def process_build(dataset, strategy, output):
    """
    Function for command 'build' is CLI

    function create inverted index on dataset and dump it in output
    dump_method = strategy
    """
    documents = load_documents(dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(output, strategy)


def callback_query(arguments):
    """ Wrapper over process_query function """
    return process_queries(
        arguments.inverted_index_filepath,
        arguments.strategy,
        arguments.query_file,
        arguments.query,
    )


def process_queries(inverted_index_filepath, strategy='struct', query_file=None, queries=None):
    """
    Function for command 'query' is CLI

    function print result of querys on load inverted index
    """
    inverted_index = InvertedIndex.load(inverted_index_filepath, strategy)
    if isinstance(query_file, list):
        query_file = query_file[0]

    if queries:
        fin = queries
    else:
        fin = query_file

    for query in fin:
        if isinstance(query, str):
            query = query.split()
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
        "-s", "--strategy", default="struct", choices=['json', 'struct'],
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
        "-i", "--index", required=True,
        help="path to store inverted index",
        dest="inverted_index_filepath",
    )
    query_parser.add_argument(
        "-s", "--strategy", choices=['json', 'struct'],
        help="format of load file", default="struct",
    )
    query_file_group = query_parser.add_mutually_exclusive_group(required=True)
    query_file_group.add_argument(
        "-q", "--query", help="set of words for query",
        action="append", nargs="+", dest="query",
    )
    query_file_group.add_argument(
        "--query-file-utf8", help="file in utf8 with query",
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
        nargs="+", dest="query_file", type=EncodedFileType('r', encoding="utf-8"),
    )
    query_file_group.add_argument(
        "--query-file-cp1251", help="file in cp1251 with query",
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        nargs="+", dest="query_file", type=EncodedFileType('r', encoding="cp1251"),
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
