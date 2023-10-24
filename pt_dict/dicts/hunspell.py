import re
from os import path

from pt_dict.constants import HUNSPELL_DIR
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.variants.variant import VARIANTS


class HunspellDict(Dictionary):
    def collect_lemmata(self, split_compounds=False):
        for variant in VARIANTS:
            self.collect_lemmata_from_file(variant.dic(), re.compile('^([^/\\t#]+)(/|$|\\t)'), split_compounds)
        return self.lemmata
