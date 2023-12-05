"""This script is used to normalise city names in the pt_BR Hunspell dictionary.

For some reason, it contains many city names complete with the state abbreviation (e.g. "Magé-RJ"), but those are just
a waste of space. This script will identify those entities and:
- if the city name (without the state abbreviation) is already present in the dictionary, we just remove the full one;
- if the city name is not in the dictionary, we replace the full one with the simple one ("Magé-RJ" to "Magé").
"""

import re
from os import replace
from tempfile import NamedTemporaryFile

from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR


class City:
    PATTERN = re.compile('^[^-]+-[A-Z]{2}$')

    def __init__(self, city_str: str):
        self.full = city_str
        parsed = city_str.split('-')
        self.name = parsed[0]
        self.state = parsed[1]

    def __str__(self) -> str:
        return self.full


def collect_lemmata() -> set[str]:
    dictionary = Dictionary()
    dictionary.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern)
    return dictionary.lemmata


def main():
    tmp_dic = NamedTemporaryFile(delete=False)
    tmp_lines = []
    lemmata = collect_lemmata()
    with open(PT_BR.dic(), 'r') as dic_file:
        for line in dic_file.readlines():
            line = line.strip()
            lemma_match = HunspellDict.pattern.match(line)
            if lemma_match:
                city_str = lemma_match.group(1)
                city_match = City.PATTERN.match(city_str)
                if city_match:
                    city = City(city_str)
                    if city.name not in lemmata:
                        tmp_lines.append(city.name)
                    else:
                        continue
                else:
                    tmp_lines.append(line)
            else:
                if line.strip() != '':
                    tmp_lines.append(line)
    with open(tmp_dic.name, 'w') as tmp_file:
        tmp_file.write("\n".join(tmp_lines))
    replace(tmp_file.name, PT_BR.dic())
    tmp_dic.close()


if __name__ == '__main__':
    main()
