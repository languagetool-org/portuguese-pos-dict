from os import path

from pt_dict.constants import TO_ADD_DIR, LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR, PT_PT_90


def print_tagged_words(words: set[str], tags: str):
    for word in words:
        print(f"{word}/{tags}")


def clean_able():
    filename = "able.txt"
    print(filename)
    filepath = path.join(TO_ADD_DIR, filename)
    pt_tags = "pms"
    br_tags = "KXIB"
    new_pt = set()
    new_br = set()
    with open(filepath, 'r') as file:
        lines = file.read().split("\n")
        for line in lines:
            if line.startswith("#") or line == '':
                continue
            word = line.strip()
            if word.endswith("is"):
                word = word[:-2] + 'l'
            if word not in BR_LEMMATA:
                new_br.add(word)
            if word not in PT_LEMMATA:
                new_pt.add(word)
    print(f"BR: {len(new_br)}")
    print_tagged_words(new_br, br_tags)
    print(f"PT: {len(new_pt)}")
    print_tagged_words(new_pt, pt_tags)


if __name__ == "__main__":
    br_dict = Dictionary()
    pt_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    pt_dict.collect_lemmata_from_file(PT_PT_90.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    BR_LEMMATA = br_dict.lemmata
    PT_LEMMATA = pt_dict.lemmata
    clean_able()
