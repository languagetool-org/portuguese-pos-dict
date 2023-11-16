import random
import re

from pt_dict.constants import COMPOUNDS_FILEPATH, LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict
from pt_dict.utils import print_sample
from pt_dict.variants.variant import PT_BR, PT_PT_45, Variant, PT_PT_90


def extract_lt_compounds() -> set[str]:
    lt_compounds = set()
    with open(COMPOUNDS_FILEPATH, 'r') as compounds_file:
        for line in compounds_file.read().split("\n"):
            if line == "" or line.startswith("#"):
                continue
            match = COMPOUNDS_PATTERN.match(line)
            if match is not None:
                compound = match.group(1)
                lt_compounds.add(compound)
    return lt_compounds


def has_hyphenated_prefix(word: str) -> bool:
    elements = word.split('-')
    if len(elements) < 2:
        return False
    return elements[0] in PREFIXES and (elements[1].startswith('r') or elements[1].startswith('s'))


def has_consonantal_prefix(word: str) -> bool:
    elements = word.split('-')
    if len(elements) < 2:
        return False
    return elements[0] in CONSONANTAL_PREFIXES and elements[1].startswith('r')


def has_dangerous_capital(word: str, lemmata: set[str]) -> bool:
    elements = word.split('-')
    danger_pattern = re.compile('^[A-ZÂÃÁÉÊÓÔÚÍ]')
    if len(elements) < 2:
        return False
    return any([danger_pattern.match(element) and
                element not in lemmata and
                element.lower() in lemmata for element in elements])


def remove_long_lemmata(lemmata: set[str]) -> set[str]:
    return set(filter(lambda lemma: len(lemma.split('-')) <= MAX_COMPOUND_SIZE, lemmata))


def prefixes_from_pt_45():
    pt_45_dict = Dictionary()
    pt_45_dict.collect_lemmata_from_file(PT_PT_45.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    hunspell_lemmata = pt_45_dict.lemmata
    hunspell_lemmata_hyphenated = set(filter(lambda lemma: has_hyphenated_prefix(lemma), hunspell_lemmata))
    hunspell_only_hyphenated_lemmata = hunspell_lemmata_hyphenated.difference(TAGGER_LEMMATA_HYPHENATED)
    lemmata_not_in_compounds_file = hunspell_only_hyphenated_lemmata.difference(LT_COMPOUNDS)
    candidate_lemmata = remove_long_lemmata(lemmata_not_in_compounds_file)
    print("compounds not in LT compounds file: ", len(candidate_lemmata))
    print_sample(list(candidate_lemmata), SAMPLE_SIZE)
    with open('new_lt_prefixed_compounds.txt', 'w') as new_lt_compounds_file:
        new_lt_compounds_file.write("\n".join(sorted([f"{lemma}?" for lemma in candidate_lemmata])))


def consonantal_prefixes():
    br_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    hunspell_lemmata = br_dict.lemmata
    hunspell_lemmata_consonantal_prefixes = set(filter(lambda lemma: has_consonantal_prefix(lemma), hunspell_lemmata))
    not_in_compounds_file = hunspell_lemmata_consonantal_prefixes.difference(LT_COMPOUNDS)
    candidate_lemmata = remove_long_lemmata(not_in_compounds_file)
    print("compounds with consonantal prefixes: ", len(candidate_lemmata))
    print_sample(list(candidate_lemmata), SAMPLE_SIZE)


def hyphenated_from_br():
    br_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    hunspell_lemmata = br_dict.lemmata
    hunspell_lemmata_hyphenated = set(filter(lambda lemma: '-' in lemma, hunspell_lemmata))
    hunspell_only_hyphenated_lemmata = hunspell_lemmata_hyphenated.difference(TAGGER_LEMMATA_HYPHENATED)
    lemmata_not_in_compounds_file = hunspell_only_hyphenated_lemmata.difference(LT_COMPOUNDS)
    candidate_lemmata = remove_long_lemmata(lemmata_not_in_compounds_file)
    print("compounds not in LT compounds file: ", len(candidate_lemmata))
    print_sample(list(candidate_lemmata), SAMPLE_SIZE)
    with open('new_lt_compounds.txt', 'w') as new_lt_compounds_file:
        new_lt_compounds_file.write("\n".join(sorted([f"{lemma}*" for lemma in candidate_lemmata])))


def uppercase_hyphenated_from_br():
    br_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    hunspell_lemmata = br_dict.lemmata
    hunspell_lemmata_dangerous = set(filter(lambda lemma: has_dangerous_capital(lemma, hunspell_lemmata),
                                            hunspell_lemmata))
    print("dangerous hyphenated: ", len(hunspell_lemmata_dangerous))
    print_sample(list(hunspell_lemmata_dangerous), SAMPLE_SIZE)
    with open('dangerous.txt', 'w') as dangerous_file:
        dangerous_file.write("\n".join(hunspell_lemmata_dangerous))


def clean_compounds(variant: Variant):
    compound_lines = []
    other_lines = []
    with open(variant.dic(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
        for line in dic_file.read().split("\n")[1:]:
            if line == '' or line.startswith('#'):
                continue
            lemma_match = HunspellDict.pattern.match(line)
            if lemma_match:
                lemma = lemma_match.group(1)
                if len(lemma.split('-')) > 1:
                    compound_lines.append(line)
                    continue
            other_lines.append(line)
    with open(variant.dic(), 'w', encoding=LATIN_1_ENCODING) as dic_file:
        dic_file.write(str(len(other_lines)) + "\n")
        dic_file.write("\n".join(other_lines))
    # with 'a' mode this messes up the line count, beware
    with open(variant.compounds(), 'a', encoding=LATIN_1_ENCODING) as compounds_file:
        compounds_file.write(str(len(compound_lines)) + "\n")
        compounds_file.write("\n".join(compound_lines))


if __name__ == "__main__":
    SAMPLE_SIZE = 100
    MAX_COMPOUND_SIZE = 5
    TAGGER_LEMMATA = TaggerDict().collect_lemmata()
    TAGGER_LEMMATA_HYPHENATED = set(filter(lambda lemma: '-' in lemma, TAGGER_LEMMATA))
    COMPOUNDS_PATTERN = re.compile("^([^*+?$]+)[*+?$]$")
    LT_COMPOUNDS = extract_lt_compounds()
    PREFIXES = {'anti', 'contra', 'multi', 'mini', 'extra', 'eletro', 'ultra', 'infra', 'auto', 'arqui', 'supra',
                'micro', 'macro'}
    CONSONANTAL_PREFIXES = {'ad', 'ab', 'sub'}

    # hyphenated_from_br()
    # prefixes_from_pt_45()
    # uppercase_hyphenated_from_br()
    # consonantal_prefixes()
    for variant in [PT_BR, PT_PT_90, PT_PT_45]:
        clean_compounds(variant)
