import re
from os import path

from pt_dict.constants import TAGGER_DICT_DIR
from pt_dict.dicts.dictionary import Dictionary


class TaggerDict(Dictionary):
    SIMPLE_PATTERN = re.compile('^.* (.*) .*$')
    COMPLEX_PATTERN = re.compile('^([^# =\\t]+)')
    FILES_TO_PROCESS = {
        ("adjectives-fdic.txt", COMPLEX_PATTERN),
        ("nouns-fdic.txt", COMPLEX_PATTERN),
        ("verbs-fdic.txt", COMPLEX_PATTERN),
        ("adverbs-lt.txt", SIMPLE_PATTERN),
        ("adv_mente-lt.txt", SIMPLE_PATTERN),
        ("propernouns-lt.txt", SIMPLE_PATTERN),
        ("resta-lt.txt", SIMPLE_PATTERN)
    }

    def collect_lemmata(self, split_compounds=False):
        for filename, pattern in self.FILES_TO_PROCESS:
            filepath = path.join(TAGGER_DICT_DIR, filename)
            self.collect_lemmata_from_file(filepath, pattern, split_compounds)
        return self.lemmata
