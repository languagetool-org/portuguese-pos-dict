from os import path
from typing import Optional, Literal

from pt_dict.constants import HUNSPELL_DIR, DICT_DIR, OUTPUT_DIR


class Variant:
    """Defines a single variant of the Portuguese language.

    Attributes:
        hyphenated: the xx-XX code of the variant
        underscored: the underscored code of the variant, i.e. xx_XX (used for Hunspell files)
        lang: just the language, i.e. 'pt'
        country: just the country, e.g. 'BR'
        association: the specific country that this variant is associated with; for example, Angolan and Mozambican
                     variants are grouped together with the European one; this may become obsolete soon as those three
                     dictionaries have been merged.
    """
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
        return path.join(OUTPUT_DIR, f"{self.hyphenated}.dict")

    def info(self, directory: Literal['source', 'target']) -> str:
        if directory == 'source':
            directory = DICT_DIR
        elif directory == 'target':
            directory = OUTPUT_DIR
        return path.join(directory, f"{self.hyphenated}.info")

    def freq(self) -> str:
        return path.join(DICT_DIR, f"{self.lang}_{self.association}_wordlist.xml")


PT_BR = Variant("pt-BR")
PT_PT = Variant("pt-PT")
PT_AO = Variant("pt-AO", "PT")
PT_MZ = Variant("pt-MZ", "PT")

VARIANTS = [PT_BR, PT_PT, PT_AO, PT_MZ]

DIC_VARIANTS = [PT_BR, PT_PT]
