"""This module amends the spaCy syllabifier for pt-BR, and defines some classes and data structures used primarily for
extracting variant information.
"""

import re
from re import Pattern

import spacy
from spacy_syllables import SpacySyllables
from typing import List, Union, Optional

import pt_dict.variants.phonology as ph


class SyllabifierException(Exception):
    pass


class Syllable:
    """Represents a single syllable.

    Attributes:
        value: The string value of the syllable
    """
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def endswith(self, pattern_str: str):
        return re.search(f"{pattern_str}$", self.value, re.IGNORECASE) is not None

    def startswith(self, pattern_str: str):
        return re.search(f"^{pattern_str}", self.value, re.IGNORECASE) is not None

    def is_accented(self):
        """Returns True if the syllable literally contains an accented grapheme (not whether it is stressed)."""
        return re.search(f"{ph.ACCENTED_VOWELS}", self.value, re.IGNORECASE) is not None

    def is_valid_rising_diphthong(self):
        """Returns True if the syllable nucleus is a valid rising diphthong, e.g. 'ia'.

        We do not check for 'ua' diphthongs since those behave differently with regards to accentuation, and they are
        also potentially problematic because of the <gu> and <qu> digraphs.
        """
        return re.search(f"i{ph.UNDERLYING_UNSTRESSED_VOWELS}{ph.STRESS_NEUTRAL_CONSONANTS}?$", self.value) is not None

    def to_hiatus(self):
        """Converts this syllable to a hiatus, i.e. two syllables split where their vowels meet."""
        syllable_candidates = re.match(f"(^.*{ph.VOWELS})({ph.VOWELS}{ph.STRESS_NEUTRAL_CONSONANTS}?)", self.value)
        return [Syllable(syllable_candidates.group(1)), Syllable(syllable_candidates.group(2))]

    def sub(self, pattern: Pattern, replacement: str):
        self.value = re.sub(pattern, replacement, self.value)

    def match(self, pattern_str: str) -> bool:
        return re.match(pattern_str, self.value, re.IGNORECASE) is not None

    def contains(self, pattern_str: str) -> bool:
        return re.search(pattern_str, self.value, re.IGNORECASE) is not None

    def letter(self, idx: int):
        """Return the idxth letter of the syllable."""
        try:
            return self.value[idx]
        except IndexError:
            return None


class Syllables:
    # TODO: move this to config somewhere
    nlp = spacy.load('pt_core_news_sm')
    nlp.add_pipe('syllables', config={'lang': 'pt_BR'})

    def __init__(self, word: str, values: Optional[str] = None):
        self.word = word
        self._vowel_start = None
        if values:
            self.values = values
        else:
            self._values = None

    def __str__(self) -> str:
        return '|'.join([syl.value for syl in self.values])

    @staticmethod
    def from_tsv_row(row: str):
        cells = row.split("\t")
        return Syllables(word=cells[0], values=cells[1])

    @property
    def vowel_start(self):
        if self._vowel_start is None:
            self._vowel_start = self.start_with_vowel(self.word)
        return self._vowel_start

    @property
    def values(self):
        if self._values is None:
            try:
                self._values = [Syllable(syllable) for syllable in self.nlp(self.clean_word(self.word))[0]._.syllables]
            except IndexError as e:
                raise SyllabifierException(f"spaCy failed to syllabify \"{self.word}\" ({e})")
            except TypeError as e:
                raise SyllabifierException(f"spaCy failed to syllabify \"{self.word}\" ({e})")
        return self._values

    @values.setter
    def values(self, syllables_str: str):
        self._values = [Syllable(syl) for syl in syllables_str.split("|")]

    def clean_word(self, word: str) -> str:
        cleaned = re.compile("['’]").sub('', word)
        if self.vowel_start:
            cleaned = 'h' + cleaned
        return cleaned

    @staticmethod
    def start_with_vowel(word: str) -> bool:
        return re.search(re.compile(f"^{ph.VOWELS}", re.IGNORECASE), word) is not None

    def to_tsv_row(self) -> str:
        return f"{self.word}\t{self}"

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
        try:
            syllables = Syllables(word)
        except TypeError as e:
            raise SyllabifierException(f"Cannot not syllabify \"{word}\" ({e}).")
        if syllables.values is None or syllables.first is None:
            raise SyllabifierException(f"Cannot not syllabify \"{word}\".")
        if syllables.first.startswith('h') and syllables.vowel_start:
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


class SyllablesFileRow:
    def __init__(self, row_str: str):
        parsed = row_str.split("\t")
        if len(parsed) != 2:
            raise SyllabifierException(f"Could not parse SyllablesFile row: {row_str}")
        self.word = parsed[0]
        self.syllables_str = parsed[1]

    def to_syllables(self):
        return Syllables(word=self.word, values=self.syllables_str)


class SyllablesFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.words: set[str] = set()
        self.rows: List[SyllablesFileRow] = []

    def read(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip() != '':
                    self.rows.append(SyllablesFileRow(line))
                    self.words.add(line.split("\t")[0])

    def write(self, syllables: List[Syllables], force_overwrite: bool = False):
        open_method = 'w' if force_overwrite else 'a'
        syllables = filter(lambda syl: syl.word not in self.words, syllables) if not force_overwrite else syllables
        with open(self.filepath, open_method, encoding='utf-8') as file:
            file.write("\n".join([syl.to_tsv_row() for syl in syllables]))
            file.write("\n")

    def to_syllables(self) -> List[Syllables]:
        return [row.to_syllables() for row in self.rows]

    def contains(self, word: str) -> bool:
        filtered = list(filter(lambda row: row.word == word, self.rows))
        return len(filtered) > 0

    def syllable_from_word(self, word: str) -> Optional[Syllables]:
        filtered = list(filter(lambda row: row.word == word, self.rows))
        if len(filtered) == 1:
            return filtered[0].to_syllables()
