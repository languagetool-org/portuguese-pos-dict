from os import path
from typing import Literal

from spylls.hunspell import Dictionary

from dict_tools.lib.constants import HUNSPELL_DIR
from dict_tools.lib.variant import Variant, PT_BR, PT_PT_90, PT_PT_45


class ConsoleUtils:
    def __init__(self, mode: Literal["main", "compounds"] = 'main'):
        self._mode: Literal["main", "compounds"] = mode
        self.br = None
        self.pt90 = None
        self.pt45 = None
        self.br_c = None
        self.pt90_c = None
        self.pt45_c = None
        self.load_dictionaries()

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, mode_name: Literal["main", "compounds"]) -> None:
        do_reload = self._mode != mode_name
        self._mode = mode_name
        if do_reload:
            self.reload()

    def compound_mode(self):
        self.mode = "compounds"

    def normal_mode(self):
        self.mode = "main"

    def load_dictionary(self, variant: Variant) -> Dictionary:
        if self.mode == 'compounds':
            dict_path = path.join(HUNSPELL_DIR, "compounds", variant.underscored)
        else:
            dict_path = path.join(HUNSPELL_DIR, variant.underscored)
        return Dictionary.from_files(dict_path)

    def load_dictionaries(self):
        self.br = self.load_dictionary(PT_BR)
        self.pt90 = self.load_dictionary(PT_PT_90)
        self.pt45 = self.load_dictionary(PT_PT_45)

    def reload(self):
        self.load_dictionaries()

    def lookup(self, word: str, reload=False) -> dict[str, bool]:
        if reload:
            self.reload()
        return {
            'br': self.br.lookup(word),
            'pt90': self.pt90.lookup(word),
            'pt45': self.pt45.lookup(word),
        }
