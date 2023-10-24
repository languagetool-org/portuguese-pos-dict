from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict

SOURCE_LEXICON_MAPPING = {
    'hunspell': HunspellDict,
    'tagger': TaggerDict
}


def get_source_dict(name: str) -> Dictionary:
    return SOURCE_LEXICON_MAPPING.get(name)()
