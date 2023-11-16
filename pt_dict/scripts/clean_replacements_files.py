import re
from os import path

from pt_dict.constants import RULES_DIR, ALTERNATIONS_DIR
from pt_dict.variants.variant import PT_BR, PT_PT_90


def main():
    alternations_filepath = path.join(ALTERNATIONS_DIR, 'pt_br.txt')
    alternations = set()
    with open(alternations_filepath, 'r') as alternations_file:
        for line in alternations_file.read().split("\n"):
            if line.startswith('#') or line == '':
                continue
            pair = line.split('=')
            alternations.update(pair)

    variants = [PT_PT_90]
    # variants = [PT_BR, PT_PT_90]
    vowel_pattern = re.compile('[êéôó]')
    for var in variants:
        replacements_filepath = path.join(RULES_DIR, var.hyphenated, "replace.txt")
        with open(replacements_filepath, 'r') as replacements_file:
            for line in replacements_file.read().split("\n"):
                if line.startswith('#') or line == '':
                    continue
                first, second = line.split("=")
                if first not in alternations and first[:-1] not in alternations:
                    print(line)
                # if not vowel_pattern.sub('', first) == vowel_pattern.sub('', second):
                #     print(line)


if __name__ == '__main__':
    main()
