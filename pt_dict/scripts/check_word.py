"""This script is here to check if a group of words is *present* in our dictionaries.

UNIMPLEMENTED: it also shows us how they're tagged and, if we pass an extra option to it, expands their inflections.
"""
import argparse
from typing import List

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from dict_tools.lib.variant import VARIANT_MAPPING


class CLI:
    prog_name = "poetry run python check_word.py"
    epilogue = "In case of problems when running this script, address a Github issue to the repository maintainer."
    description = "This script performs a quick lookup in all of our source dictionaries."

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=self.description,
            epilog=self.epilogue,
            formatter_class=argparse.RawTextHelpFormatter
        )

        self.parser.add_argument('words', nargs='+', help='List of words to check')
        self.parser.add_argument('--unmunch', action='store_true', default=False)
        self.args = self.parser.parse_args()


class LookUp:
    def __init__(self, words: List[str]):
        self.words = words
        self.lemmata: dict[str: set[str]] = {}
        self.load_lemmata()

    def load_lemmata(self):
        for variant in DIC_VARIANTS:
            dictionary = Dictionary()
            for filepath in [variant.dic(), variant.compounds()]:
                dictionary.collect_lemmata_from_file(filepath, HunspellDict.pattern, encoding=LATIN_1_ENCODING,
                                                     offset=1)
            self.lemmata[variant.hyphenated_with_agreement] = dictionary.lemmata

    def find_word(self, word: str):
        print(f"\"{word}\":")
        for variant, lemmata in self.lemmata.items():
            print(f"{variant}: {word in lemmata}")

    def run(self):
        for word in self.words:
            self.find_word(word)


if __name__ == '__main__':
    cli = CLI()
    DIC_VARIANTS = VARIANT_MAPPING.get('pt')
    LookUp(cli.args.words).run()
