import re
from os import path
from typing import Callable

from pt_dict.constants import TO_ADD_DIR, LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR, PT_PT_90, Variant


def tag_word(word: str, tags: str) -> str:
    if tags == '':
        return word
    return f"{word}/{tags}"


def tag_words(words: set[str], tags: str) -> set[str]:
    return set([f"{tag_word(word, tags)}" for word in words])


def new_lookup(br_tags: str, pt_tags: str) -> dict:
    return {
        'pt-BR': {
            'tags': br_tags,
            'new_words': set()
        },
        'pt-PT': {
            'tags': pt_tags,
            'new_words': set()
        }
    }


def collect_words_from_file(filepath: str, normaliser: Callable) -> set[str]:
    words = set()
    with open(filepath, 'r') as file:
        lines = file.read().split("\n")
        for line in lines:
            if line.startswith("#") or line == '':
                continue
            words.add(normaliser(line.strip()))
    return words


def add_word(word: str, variant: Variant, lookup: dict):
    if word not in LEMMATA[variant.hyphenated]:
        lookup[variant.hyphenated]['new_words'].add(word)


def process_file(filename: str, br_tags: str, pt_tags: str, normaliser: Callable):
    print(filename)
    filepath = path.join(TO_ADD_DIR, filename)
    lookup = new_lookup(br_tags, pt_tags)
    words = collect_words_from_file(filepath, normaliser)
    for variant in VARIANTS:
        for word in words:
            add_word(word, variant, lookup)

        new_words = lookup[variant.hyphenated]['new_words']
        tags = lookup[variant.hyphenated]['tags']
        print(f"{variant.country}: {len(new_words)}")
        tagged = tag_words(new_words, tags)
        print("\n".join(tagged))
        if not DRY_RUN:
            add_to_dic(tagged, variant)


def add_to_dic(words: set[str], variant: Variant):
    lines = []
    with open(variant.dic(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
        lines.extend(dic_file.read().split("\n")[1:])
    lines.extend(words)  # preserve order
    with open(variant.dic(), 'w', encoding=LATIN_1_ENCODING) as dic_file:
        dic_file.write(str(len(lines)) + "\n")
        dic_file.write("\n".join(lines))


def clean_able():
    def normaliser(w: str) -> str:
        if w.endswith("is"):
            return w[:-2] + 'l'
        return w
    process_file('able.txt', 'KXIB', 'pms', normaliser)


def clean_ador():
    def normaliser(w: str) -> str:
        return re.compile('([aei]dor)(es|as?)?$').sub(r"\1", w)
    process_file('ador.txt', 'DR', 'fp', normaliser)


def clean_adverbs():
    process_file('adverbs.txt', '', '', lambda w: w)


def clean_orio():
    def normaliser(w: str) -> str:
        return re.compile('(óri)[oa]s?$').sub(r"\1o", w)
    process_file('orio.txt', 'D', 'fp', normaliser)


if __name__ == "__main__":
    VARIANTS = [PT_BR, PT_PT_90]
    br_dict = Dictionary()
    pt_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    pt_dict.collect_lemmata_from_file(PT_PT_90.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    LEMMATA = {
        'pt-BR': br_dict.lemmata,
        'pt-PT': pt_dict.lemmata
    }
    DRY_RUN = False
    # clean_able()
    # clean_ador()
    # clean_adverbs()
    clean_orio()
