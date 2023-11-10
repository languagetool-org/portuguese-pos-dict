import re

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.variants.variant import VARIANTS


class HunspellDict(Dictionary):
    pattern = re.compile('^([^/\\t#]+)(/|$|\\t)')

    def collect_lemmata(self, split_compounds=False):
        for variant in VARIANTS:
            self.collect_lemmata_from_file(variant.dic(), self.pattern, split_compounds, encoding=LATIN_1_ENCODING,
                                           offset=1)
        return self.lemmata
