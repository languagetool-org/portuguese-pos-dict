import re
from typing import List


class Dictionary:
    def __init__(self):
        self._lemmata: set[str] = set()

    @property
    def lemmata(self):
        return self._lemmata

    def collect_lemmata_from_file(self, filepath: str, pattern: re.Pattern, split_compounds=False, encoding="utf-8"):
        """Define a function to process a file and collect lemmata."""
        with open(filepath, 'r', encoding=encoding) as file:
            for line in file:
                match = re.match(pattern, line.strip())
                if match:
                    lemma = match.group(1)
                    if split_compounds:
                        self.lemmata.update(lemma.split('-'))
                    else:
                        self.lemmata.add(lemma)

    def collect_lemmata(self, split_compounds=False):
        pass
