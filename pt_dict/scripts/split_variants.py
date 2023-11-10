"""This module makes sure the pt_BR_90, pt_PT_45, and pt_PT_90 hunspell dictionaries contain appropriate forms."""
import re
from typing import List, Literal
from tqdm import tqdm

from pt_dict.constants import LATIN_1_ENCODING, PT_BR_ALTERNATIONS_FILEPATH, PT_45_90_ALTERNATIONS_FILEPATH
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_PT_45, PT_PT_90, PT_BR, Variant


def write_lines_to_dic(variant: Variant, new_lines: List[str]):
    with open(variant.dic(), 'w', encoding=LATIN_1_ENCODING) as dic_file:
        dic_file.write(str(len(new_lines)) + "\n")
        dic_file.write("\n".join(new_lines))


SUFFIX_MAPPING = {
    'noun': {'pt-BR': 'B', 'pt-PT': 'p'},
    'oa_adj': {'pt-BR': 'DJH', 'pt-PT': 'fpm'},
    'e_adj': {'pt-BR': 'BJH', 'pt-PT': 'pm'},
}

ADJ_SUFFIXES = ['ico', 'neo']
NOUN_SUFFIXES = ['[êé]ni[oa]', 'id[ea]']


def suffix_pattern(suffixes: List[str]) -> re.Pattern:
    return re.compile(f"({'|'.join(suffixes)})$")


def new_hunspell_line(lemma: str, variant: Variant) -> str:
    def suffixed_line(suffix_name: str) -> str:
        return f"{lemma}/{SUFFIX_MAPPING[suffix_name][variant.hyphenated]}"
    # not messing with compounds
    if '-' in lemma or ' ' in lemma:
        return lemma
    if suffix_pattern(ADJ_SUFFIXES).search(lemma):
        return suffixed_line('oa_adj')
    elif suffix_pattern(NOUN_SUFFIXES).search(lemma):
        return suffixed_line('noun')
    elif lemma.endswith('s'):  # invariable
        return lemma
    else:
        return suffixed_line('noun')


def variantise_file(variant: Variant, all_forms: set[str], good_forms: set[str], bad_forms: set[str],
                    bad_to_good_lookup: dict[str: str], lookup_style: Literal['symmetric', 'no_bad', 'many_bad']):
    new_lines = []
    with open(variant.dic(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
        lines = tqdm(dic_file.read().split("\n")[1:])
        lines.set_description(variant.hyphenated_with_agreement)
        relevant_lemmata = set()
        for line in lines:
            lemma_match = HunspellDict.pattern.match(line)
            if lemma_match:
                lemma = lemma_match.group(1)
            if lemma_match is None or lemma not in all_forms:
                new_lines.append(line)
                continue
            if lemma in good_forms:
                if line not in new_lines:
                    new_lines.append(line)
                    relevant_lemmata.add(lemma)
                    continue
            if lookup_style == 'symmetric':
                if lemma in bad_forms:
                    new_line = re.sub(re.compile(f"^{lemma}"), bad_to_good_lookup[lemma], line)
                    if new_line not in new_lines:
                        new_lines.append(new_line)
                        relevant_lemmata.add(lemma)
            elif lookup_style == 'many_bad':
                if lemma in bad_forms:
                    good_alternatives = bad_to_good_lookup[lemma].split(",")
                    if len(good_alternatives) == 1:
                        new_lemma = good_alternatives[0]
                        new_line = re.sub(re.compile(f"^{lemma}"), new_lemma, line)
                        if new_line not in new_lines:
                            new_lines.append(new_line)
                            relevant_lemmata.add(new_lemma)
                    else:
                        for alternative in good_alternatives:
                            new_line = re.sub(re.compile(f"^{lemma}"), alternative, line)
                            if new_line not in new_lines:
                                new_lines.append(new_line)
                                relevant_lemmata.add(alternative)
            elif lookup_style == 'no_bad':
                continue
    # get all entries from alternation file that *aren't* in the lexicon at all and add them at the end of the file...
    for new_lemma in good_forms.difference(relevant_lemmata):
        new_lines.append(new_hunspell_line(new_lemma, variant))
    write_lines_to_dic(variant, new_lines)


def split_dialects():
    """Perform the BR <=> PT alternation."""
    br_forms = set()
    pt_forms = set()
    alternations: set[tuple[str, str]] = set()
    with open(PT_BR_ALTERNATIONS_FILEPATH, 'r') as two_way_file:
        for br_form, pt_form in [line.split('=') for line in two_way_file.read().split('\n')]:
            alternations.add((br_form, pt_form))
            br_forms.add(br_form)
            pt_forms.add(pt_form)
    br_alternations = dict(alternations)
    pt_alternations = dict([(pt, br) for br, pt in alternations])
    all_forms = br_forms.union(pt_forms)
    variantise_file(PT_BR, all_forms, br_forms, pt_forms, pt_alternations, lookup_style='symmetric')
    variantise_file(PT_PT_90, all_forms, pt_forms, br_forms, br_alternations, lookup_style='symmetric')
    variantise_file(PT_PT_45, all_forms, pt_forms, br_forms, br_alternations, lookup_style='symmetric')


def split_agreements():
    """Perform the 45 <=> 90 pt-PT alternation."""
    ao90_forms = set()
    ao45_forms = set()
    alternations: set[tuple[str, str]] = set()
    with open(PT_45_90_ALTERNATIONS_FILEPATH, 'r') as two_way_file:
        for ao45_form, ao90_form in [line.split("\t") for line in two_way_file.read().split('\n')]:
            alternations.add((ao45_form, ao90_form))
            # I think it'll be better to do this than to have duplicates, actually...
            split90 = [form.strip() for form in ao90_form.split(',')]
            ao90_forms.update(split90)
            ao45_forms.add(ao45_form)
    ao45_alternations = dict(alternations)
    ao90_alternations = dict([(ao90, ao45) for ao45, ao90 in alternations])
    all_forms = ao45_forms.union(ao90_forms)
    variantise_file(PT_PT_90, all_forms, ao90_forms, ao45_forms, ao45_alternations, lookup_style='many_bad')
    # all 45 forms already in the dictionary and among the ao90 forms, no need to reverse the check
    variantise_file(PT_PT_45, all_forms, ao45_forms, ao90_forms, ao90_alternations, lookup_style='no_bad')


if __name__ == '__main__':
    split_dialects()
    split_agreements()
