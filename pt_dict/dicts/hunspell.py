import re

from dict_tools.lib.constants import LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from dict_tools.lib.variant import VARIANT_MAPPING


class HunspellDict(Dictionary):
    pattern = re.compile('^([^/\\t#]+)(/|$|\\t)')

    def collect_lemmata(self, split_compounds=False):
        for variant in VARIANT_MAPPING.get('pt'):
            self.collect_lemmata_from_file(variant.dic(), self.pattern, split_compounds, encoding=LATIN_1_ENCODING,
                                           offset=1)
        return self.lemmata
