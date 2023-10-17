"""This module does a hacky implementation of a FOMA-powered pt-BR syllabifier, since the Python bindings don't work."""
import re
from re import Pattern

import spacy
from spacy_syllables import SpacySyllables
from typing import List, Union

import variants.phonology as ph


class Syllable:
    def __init__(self, value: str):
        self.value = value

    def endswith(self, pattern_str: str):
        return re.search(f"{pattern_str}$", self.value, re.IGNORECASE) is not None

    def startswith(self, pattern_str: str):
        return re.search(f"^{pattern_str}", self.value, re.IGNORECASE) is not None

    def is_accented(self):
        return re.search(f"{ph.ACCENTED_VOWELS}", self.value, re.IGNORECASE) is not None

    def is_valid_rising_diphthong(self):
        return re.search(f"i{ph.UNDERLYING_UNSTRESSED_VOWELS}{ph.STRESS_NEUTRAL_CONSONANTS}?$", self.value) is not None

    def to_hiatus(self):
        syllable_candidates = re.match(f"(^.*{ph.VOWELS})({ph.VOWELS}{ph.STRESS_NEUTRAL_CONSONANTS}?)", self.value)
        return [Syllable(syllable_candidates.group(1)), Syllable(syllable_candidates.group(2))]

    def sub(self, pattern: Pattern, replacement: str):
        self.value = re.sub(pattern, replacement, self.value)

    def match(self, pattern_str: str) -> bool:
        return re.match(pattern_str, self.value, re.IGNORECASE) is not None

    def contains(self, pattern_str: str) -> bool:
        return re.search(pattern_str, self.value, re.IGNORECASE) is not None

    def letter(self, idx: int):
        try:
            return self.value[idx]
        except IndexError:
            return None


class Syllables:
    # TODO: move this to config somewhere
    nlp = spacy.load('pt_core_news_sm')
    nlp.add_pipe('syllables', config={'lang': 'pt_BR'})

    def __init__(self, word: str):
        self.values = [Syllable(syllable) for syllable in self.nlp(word)[0]._.syllables]

    def get_by_index(self, idx: int):
        try:
            return self.values[idx]
        except IndexError:
            return None

    def set_by_index(self, idx: int, value: Union[str, Syllable]):
        if isinstance(value, str):
            new_syllable = Syllable(value)
        else:
            new_syllable = value
        try:
            self.values[idx] = new_syllable
        except IndexError:
            return None

    def add(self, new_syllable: Syllable):
        self.values.append(new_syllable)

    def delete_last(self):
        self.values.pop(-1)

    @property
    def size(self):
        return len(self.values)

    @property
    def first(self):
        return self.get_by_index(0)

    @first.setter
    def first(self, value: str):
        self.set_by_index(0, value)

    @property
    def last(self):
        return self.get_by_index(-1)

    @last.setter
    def last(self, value: Union[str, Syllable]):
        self.set_by_index(-1, value)

    @property
    def penultimate(self):
        return self.get_by_index(-2)

    @penultimate.setter
    def penultimate(self, value: str):
        self.set_by_index(-2, value)

    @property
    def antepenultimate(self):
        return self.get_by_index(-3)

    @antepenultimate.setter
    def antepenultimate(self, value: str):
        self.set_by_index(-3, value)


class Syllabifier:
    @staticmethod
    def is_hiatus(syllable_1: Syllable, syllable_2: Syllable):
        return syllable_1.endswith(ph.VOWELS) and syllable_2.startswith(ph.VOWELS)

    @staticmethod
    def syllabify(word: str) -> Syllables:
        vowel_start = False
        spacy_word = word
        if re.search(re.compile(f"^{ph.VOWELS}", re.IGNORECASE), word):
            vowel_start = True
            spacy_word = 'h' + word
        syllables = Syllables(spacy_word)
        if syllables.first.startswith('h') and vowel_start:
            syllables.first.sub(re.compile('^h', re.IGNORECASE), '')
        if syllables.last.is_valid_rising_diphthong() and \
                (syllables.size == 1 or not syllables.penultimate.is_accented()):
            hiatus = syllables.last.to_hiatus()
            syllables.last = hiatus[0]
            syllables.add(hiatus[1])
        if syllables.size > 2 and \
                syllables.penultimate.endswith('i') and \
                syllables.last.match(f"{ph.UNDERLYING_UNSTRESSED_VOWELS}[{ph.STRESS_NEUTRAL_CONSONANTS}]?") \
                and syllables.antepenultimate.is_accented():
            syllables.penultimate = syllables.penultimate.value + syllables.last.value
            syllables.delete_last()
        return syllables
