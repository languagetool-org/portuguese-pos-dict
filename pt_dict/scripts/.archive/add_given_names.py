import unicodedata
from os import path

from pt_dict.constants import LATIN_1_ENCODING, DATA_DIR
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR


def clean_name(name: str) -> str:
    return name.strip().replace("’", "'").replace("−", "-")


def name_is_valid(name: str) -> bool:
    return name != "" and name not in PT_BR_LEMMATA and name.lower() not in PT_BR_LEMMATA_DOWNCASED


def strip_accents(word: str):
    return ''.join(category for category in unicodedata.normalize('NFD', word)
                   if unicodedata.category(category) != 'Mn')


def name_needs_accent(name: str) -> bool:
    return strip_accents(name).lower() in PT_BR_LEMMATA_ACCENTLESS


def add_name(name: str):
    cleaned_name = clean_name(name)
    if name_is_valid(cleaned_name):
        NAMES.add(cleaned_name)
    else:
        DISCARDED_NAMES.add(cleaned_name)


if __name__ == '__main__':
    PREPOSITIONAL_THINGIES = {'de', 'do', 'da', 'dos', 'das'}

    FILEPATH = path.join(DATA_DIR, 'misc', "names.txt")

    ACCENTED_FILEPATH = path.join(DATA_DIR, 'misc', "accented_names.txt")
    NON_ACCENTED_FILEPATH = path.join(DATA_DIR, 'misc', "non_accented_names.txt")
    DISCARDED_FILEPATH = path.join(DATA_DIR, 'misc', "discarded_names.txt")

    NAMES = set()
    NAMES_THAT_NEED_ACCENT = set()
    DISCARDED_NAMES = set()

    PT_BR_DICT = Dictionary()
    PT_BR_DICT.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, offset=1, encoding=LATIN_1_ENCODING)
    PT_BR_LEMMATA = PT_BR_DICT.lemmata
    PT_BR_LEMMATA_DOWNCASED = set([lemma.lower() for lemma in PT_BR_LEMMATA])
    PT_BR_LEMMATA_ACCENTLESS = set([strip_accents(lemma) for lemma in PT_BR_LEMMATA_DOWNCASED])

    with open(FILEPATH, 'r') as names_file:
        for name in names_file.read().split("\n"):
            add_name(name)
    for prep in PREPOSITIONAL_THINGIES:
        NAMES.discard(prep)

    NEW_NAMES = NAMES.copy()
    for name in NAMES:
        if name_needs_accent(name):
            NAMES_THAT_NEED_ACCENT.add(name)
            NEW_NAMES.discard(name)

    print(f"new names: {len(NEW_NAMES)}")
    print(f"accentless new names: {len(NAMES_THAT_NEED_ACCENT)}")
    print(sorted(NAMES_THAT_NEED_ACCENT))

    with open(NON_ACCENTED_FILEPATH, 'w') as non_accented_file:
        non_accented_file.write("\n".join(sorted(NEW_NAMES)))

    with open(ACCENTED_FILEPATH, 'w') as accented_file:
        accented_file.write("\n".join(sorted(NAMES_THAT_NEED_ACCENT)))

    with open(DISCARDED_FILEPATH, 'w') as discarded_file:
        discarded_file.write("\n".join(sorted(DISCARDED_NAMES)))

    # with open(PT_BR.dic(), 'a', encoding=LATIN_1_ENCODING) as dic_file:
    #     dic_file.write("\n")
    #     dic_file.write("\n".join(names))
