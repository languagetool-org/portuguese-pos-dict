from os import path
from typing import Optional, Literal

from pt_dict.constants import HUNSPELL_DIR, DICT_DIR, OUTPUT_DIR


class Variant:
    def __init__(self, locale_code: str, country_association: Optional[str] = None):
        parsed = locale_code.split('-')
        self.hyphenated = locale_code
        self.underscored = locale_code.replace('-', '_')
        self.lang = parsed[0]
        self.country = parsed[1]
        if country_association is None:
            self.association = self.country
        else:
            self.association = country_association

    def __str__(self) -> str:
        return self.hyphenated

    def aff(self) -> str:
        return path.join(HUNSPELL_DIR, f"{self.underscored}.aff")

    def dic(self) -> str:
        return path.join(HUNSPELL_DIR, f"{self.underscored}.dic")

    def dict(self) -> str:
        return path.join(OUTPUT_DIR, f"{self.hyphenated}.dic")

    def info(self, directory: Literal['source', 'target']) -> str:
        if directory == 'source':
            directory = DICT_DIR
        elif directory == 'target':
            directory = OUTPUT_DIR
        return path.join(directory, f"{self.hyphenated}.info")

    def freq(self) -> str:
        return path.join(DICT_DIR, f"{self.lang}_{self.association}_wordlist.xml")


VARIANTS = [
    Variant("pt-BR"),
    Variant("pt-PT"),
    Variant("pt-AO", "PT"),
    Variant("pt-MZ", "PT"),
]
