from typing import List

import random

from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict

SOURCE_LEXICON_MAPPING = {
    'hunspell': HunspellDict,
    'tagger': TaggerDict
}


def get_source_dict(name: str) -> Dictionary:
    return SOURCE_LEXICON_MAPPING.get(name)()


def print_sample(word_list: List[str], sample_size: int):
    print(', '.join(sorted(word_list, key=lambda i: random.random())[0:sample_size]))
