from os import path

from pt_dict.constants import REPO_DIR, LATIN_1_ENCODING, DATA_DIR
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR

filepath = path.join(DATA_DIR, 'misc', "fuvest_n.txt")

names = set()

PT_BR_DICT = Dictionary()
PT_BR_DICT.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, offset=1, encoding=LATIN_1_ENCODING)
PT_BR_LEMMATA = PT_BR_DICT.lemmata


def clean_name(name: str) -> str:
    return name.strip().replace("’", "'").replace("−", "-")


def name_is_valid(name: str) -> bool:
    return name != "" and name not in PT_BR_LEMMATA


def add_name(name: str):
    cleaned_name = clean_name(name)
    if name_is_valid(cleaned_name):
        names.add(cleaned_name)


with open(filepath, 'r') as names_file:
    for name in names_file.read().split(" "):
        add_name(name)

print(names)

# with open(PT_BR.dic(), 'a', encoding=LATIN_1_ENCODING) as dic_file:
#     dic_file.write("\n")
#     dic_file.write("\n".join(names))
