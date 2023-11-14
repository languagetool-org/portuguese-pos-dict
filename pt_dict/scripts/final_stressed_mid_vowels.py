import re

from typing import List

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR, PT_PT_90, Variant


def filter_vowels(lemmata: set[str]) -> set[str]:
    vowel_pattern = re.compile("[éêóô]$")
    return set(filter(lambda lemma: vowel_pattern.search(lemma) is not None, lemmata))


def convert_vowel(lemma: str) -> str:
    stem = lemma[:-1]
    if lemma.endswith('é'):
        return stem + 'ê'
    if lemma.endswith('ê'):
        return stem + 'é'
    if lemma.endswith('ó'):
        return stem + 'ô'
    if lemma.endswith('ô'):
        return stem + 'ó'


def is_grandparent(lemma: str) -> bool:
    grandparent_pattern = re.compile("^(bis|tr[ie]s|tetr|pent|tatar)?av[ôó]$|^vov[óô]$")
    return grandparent_pattern.match(lemma) is not None


def collect_hunspell_lemmata(variant: Variant) -> set[str]:
    dictionary = Dictionary()
    dictionary.collect_lemmata_from_file(variant.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    return dictionary.lemmata


def main():
    br_lemmata = filter_vowels(collect_hunspell_lemmata(PT_BR))
    pt_lemmata = filter_vowels(collect_hunspell_lemmata(PT_PT_90))
    all_lemmata = br_lemmata.union(pt_lemmata)
    lemma_table: List[tuple[set[str], set[str]]] = []
    checked = set()
    for lemma in all_lemmata:
        if is_grandparent(lemma):
            continue
        converted_lemma = convert_vowel(lemma)
        if converted_lemma in checked:
            continue
        checked.add(lemma)
        checked.add(converted_lemma)

        if converted_lemma not in all_lemmata:
            continue
        pair: tuple[set[str], set[str]] = (set(), set())
        br_accept: set[str] = set()
        pt_accept: set[str] = set()
        if lemma in br_lemmata:
            br_accept.add(lemma)
        if lemma in pt_lemmata:
            pt_accept.add(lemma)
        if converted_lemma in br_lemmata:
            br_accept.add(converted_lemma)
        if converted_lemma in pt_lemmata:
            pt_accept.add(converted_lemma)
        if all([len(accept) > 0 for accept in [br_accept, pt_accept]]):
            pair = (br_accept, pt_accept)
            lemma_table.append(pair)
    print(len(lemma_table))
    for pair in sorted(lemma_table, key=lambda p: list(p[0])[0]):
        print(pair)


if __name__ == '__main__':
    main()
