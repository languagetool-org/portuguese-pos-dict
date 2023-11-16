import re

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.utils import print_sample
from pt_dict.variants.variant import PT_BR


def main():
    br_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    br_lemmata = br_dict.lemmata
    dupes = set()
    for lemma in br_lemmata:
        if re.compile("^[A-ZÁÂÃÉÊÓÔÕÚÍÇ]").match(lemma) and lemma.lower() in br_lemmata:
            dupes.add(lemma)
    print(f"number of dupes: {len(dupes)}")
    print_sample(list(dupes), 100)


if __name__ == '__main__':
    main()
