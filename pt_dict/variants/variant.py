from os import path
from typing import Optional, Literal

from pt_dict.constants import HUNSPELL_DIR, DICT_DIR, OUTPUT_DIR, COMPOUNDS_DIR


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
        agreement: which specific orthography agreement to use, 1945 or 1990; the default is 90.
    """
    def __init__(self, locale_code: str, country_association: Optional[str] = None,
                 agreement: Literal['45', '90'] = '90'):
        parsed = locale_code.split('-')
        self.agreement = agreement
        self.hyphenated = locale_code
        self.hyphenated_with_agreement = f"{self.hyphenated}-{self.agreement}"
        self.underscored = locale_code.replace('-', '_')
        self.underscored_with_agreement = f"{self.underscored}_{self.agreement}"
        self.lang = parsed[0]
        self.country = parsed[1]
        if country_association is None:
            self.association = self.country
        else:
            self.association = country_association

    def __str__(self) -> str:
        if self.country == 'PT':
            return self.hyphenated_with_agreement
        return self.hyphenated

    def aff(self) -> str:
        if self.country == 'PT':
            filename = self.underscored_with_agreement
        else:
            filename = self.underscored
        return path.join(HUNSPELL_DIR, f"{filename}.aff")

    def dic(self) -> str:
        """Path to the plaintext Hunspell file. For pt-PT, includes the agreement."""
        if self.country == 'PT':
            filename = f"{self.underscored_with_agreement}.dic"
        else:
            filename = f"{self.underscored}.dic"
        return path.join(HUNSPELL_DIR, filename)

    def dict(self) -> str:
        """Path to the BINARY. For pt-PT, includes the agreement."""
        if self.country == 'PT':
            filename = f"{self.hyphenated_with_agreement}.dict"
        else:
            filename = f"{self.hyphenated}.dict"
        return path.join(OUTPUT_DIR, filename)

    def info(self, directory: Literal['source', 'target']) -> str:
        """The path to the info file can be in the source (current repo) or destination (the java src).

        In the case of pt-PT, there is only a single pt-PT.info file in the source, but in the destination we duplicate
        them with the full name containing agreement, due to how Morfologik files are treated in LT: the info file must
        have the same basename as the binary dic file.
        """
        filename = f"{self.hyphenated}.info"
        if directory == 'source':
            directory = DICT_DIR
        elif directory == 'target':
            directory = OUTPUT_DIR
        if self.country == 'PT':
            filename = f"{self.hyphenated_with_agreement}.info"
        return path.join(directory, filename)

    def compounds(self) -> str:
        if self.country == 'PT':
            filename = self.underscored_with_agreement
        else:
            filename = self.underscored
        return path.join(COMPOUNDS_DIR, f"{filename}.dic")

    def freq(self) -> str:
        return path.join(DICT_DIR, f"{self.lang}_{self.association}_wordlist.xml")


PT_BR = Variant("pt-BR")
PT_PT_90 = Variant("pt-PT", agreement="90")
PT_PT_45 = Variant("pt-PT", agreement="45")
PT_AO = Variant("pt-AO", "PT", "45")
PT_MZ = Variant("pt-MZ", "PT", "45")

VARIANTS = [PT_BR, PT_PT_90, PT_PT_45, PT_AO, PT_MZ]

DIC_VARIANTS = [PT_BR, PT_PT_90, PT_PT_45]
