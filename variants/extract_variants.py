"""Extract differences between PT varieties."""
from re import Pattern

from tqdm import tqdm
import re
from typing import List

from variants.syllabifier import Syllabifier
from variants.alternation import AlternationContext, Alternation

SYLLABIFIER = Syllabifier()

FILES_TO_PROCESS_COMPLEX = {
    "adjectives-fdic.txt", "nouns-fdic.txt", "verbs-fdic.txt"
}

FILES_TO_PROCESS_SIMPLE = {
    "adverbs-lt.txt", "adv_mente-lt.txt", "propernouns-lt.txt", "resta-lt.txt"
}

alternations = [
    Alternation(AlternationContext('ê', 'vowel', SYLLABIFIER), 'é', []),
    Alternation(AlternationContext('ô', 'vowel', SYLLABIFIER), 'ó', []),
    Alternation(AlternationContext('pt', 'contains', SYLLABIFIER), 't', []),
    Alternation(AlternationContext('cç', 'contains', SYLLABIFIER), 'ç', []),
    Alternation(AlternationContext('ct', 'contains', SYLLABIFIER), 't', []),
    Alternation(AlternationContext('pç', 'contains', SYLLABIFIER), 'ç', []),
]


def process_file(filename: str, pattern: Pattern) -> List[str]:
    """Define a function to process a file and collect lemmata."""
    lemmata = []
    with open(f"../src-dict/{filename}", 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                lemmata.append(match.group(1))
    return lemmata


def collect_lemmata() -> set[str]:
    lemmata = []
    for filepath in FILES_TO_PROCESS_SIMPLE:
        lemmata.extend(process_file(filepath, re.compile('^.* (.*) .*$')))
    for filepath in FILES_TO_PROCESS_COMPLEX:
        lemmata.extend(process_file(filepath, re.compile('^([^# =]+)')))
    return set(lemmata)


LEMMATA = sorted(collect_lemmata())
for lemma in tqdm(LEMMATA):
    for alternation in alternations:
        try:
            alternation.transform(lemma)
        except TypeError as e:
            print(f"\"{lemma}\": {e}")

TRANSFORMATIONS = []
for alternation in alternations:
    transformations = filter(lambda transformation: transformation.target in LEMMATA, alternation.transformations)
    TRANSFORMATIONS.extend(transformations)

with open('br-pt.txt', 'a', encoding='utf-8') as output_file:
    output_file.write("\n".join([transformation.__str__() for transformation in TRANSFORMATIONS]))
