"""This script tests to see if words are recognised by the Hunspell binary, using our Hunspell source files."""
import sys
from os import path

from spylls.hunspell import Dictionary

from pt_dict.constants import HUNSPELL_DIR
from pt_dict.variants.variant import PT_BR


def main():
    COMPOUND = True
    absent: dict[str, set] = dict()
    present: dict[str, set] = dict()
    words = set()
    test_filepath = sys.argv[1]
    loop_variants = [PT_BR]
    with open(test_filepath, 'r') as test_file:
        words.update(test_file.read().split("\n"))
    for variant in loop_variants:
        print(f"Checking {variant}...")
        if variant.country == 'BR':
            variant_code = variant.underscored
        else:
            variant_code = variant.underscored_with_agreement
        absent[variant_code] = set()
        present[variant_code] = set()
        if COMPOUND:
            dict_path = path.join(HUNSPELL_DIR, "compounds", variant_code)
        else:
            dict_path = path.join(HUNSPELL_DIR, variant_code)
        dictionary = Dictionary.from_files(dict_path)
        for word in words:
            if dictionary.lookup(word):
                present[variant_code].add(word)
            else:
                absent[variant_code].add(word)
        print(f"Present: {len(present[variant_code])}")
        print(f"Absent: {len(absent[variant_code])}")
    present_in_all = set.intersection(*present.values())
    absent_in_all = set.intersection(*absent.values())
    print(f"Present in all: {len(present_in_all)}")
    print(f"Absent in all: {len(absent_in_all)}")
    # print("OOGA")
    # print("\n".join(sorted(words.difference(absent_in_all))))
    # print("FRED")
    print("\n".join(sorted(absent_in_all)))
    # print("\n".join(sorted(words.difference(present_in_all))))


if __name__ == "__main__":
    main()
