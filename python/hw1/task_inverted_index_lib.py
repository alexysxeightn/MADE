from __future__ import annotations

from typing import Dict, List
import re
import pickle


class InvertedIndex:
    def __init__(self, documents: Dict[str, List[int]]):
        self._data = documents

    def __eq__(self, other: InvertedIndex):
        if self._data is None or other._data is None:
            return False
        k1 = {k: sorted(v) for k, v in self._data.items()}
        k2 = {k: sorted(v) for k, v in other._data.items()}
        return k1 == k2


    def query(self, words: List[str]) -> List[int]:
        """Return the list of relevant documents for the given query"""
        words = [word.lower() for word in words]
        if words[0] not in self._data.keys():
            return []
        else:
            answer = set(self._data[words[0]])
            for word in words:
                word = word
                if word not in self._data.keys():
                    return [] 
                answer = answer & set(self._data[word])
            return list(answer)

    def dump(self, filepath: str) -> None:
        with open(filepath, 'wb') as f:
            pickle.dump(self._data, f)

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        with open(filepath, 'rb') as f:
            docs = pickle.load(f)
            return cls(documents = docs)


def load_documents(filepath: str) -> Dict[int, str]:
    documents = dict()

    with open(filepath) as file:
        file_content = file.readlines()

    for line in file_content:
        doc_id, content = line.lower().split("\t", 1)
        doc_id = int(doc_id)
        documents[doc_id] = content.strip()

    return documents


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    inverted_index = dict()
    for key in documents.keys():
        for word in set(re.split(r"\W+", documents[key])):
            if word in inverted_index.keys():
                inverted_index[word].append(key)
            else:
                inverted_index[word] = [key] 
    return InvertedIndex(inverted_index)

def main():
    documents = load_documents("/path/to/dataset")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("/path/to/inverted.index")
    inverted_index = InvertedIndex.load("/path/to/inverted.index")
    document_ids = inverted_index.query(["two", "words"])


if __name__ == "__main__":
    main()
