"""This script merges the PT, AO, and MZ dictionary files into a single DIC file.

This is possible because the affix definitions for all three varieties are the same, but we can't merge uncritically
because sometimes entries have different flags. For example, frequently nouns in the pt_PT dictionary have diminutive
flags, whereas those in the AO/MZ ones don't. If we just brute-forced them together, we'd end up with duplicated entries
differing only in the flags.
"""

from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_AO, PT_MZ, PT_PT, Variant


def iterate_over_african_dictionary(variant: Variant, lemmata: set[str]):
    new_lines: set[str] = set()
    with open(variant.dic(), 'r', encoding="ISO-8859-1") as dic_file:
        for line in dic_file.readlines():
            line = line.strip()
            lemma_match = HunspellDict.pattern.match(line)
            if lemma_match is not None:
                lemma = lemma_match.group(1)
                if lemma not in lemmata:
                    lemmata.add(lemma)
                    new_lines.add(line)
    return new_lines


def main():
    pt_dic = Dictionary()
    pt_dic.collect_lemmata_from_file(PT_PT.dic(), HunspellDict.pattern, encoding="ISO-8859-1")
    pt_lemmata = pt_dic.lemmata
    print(f"Initial number of lemmata: {len(pt_lemmata)}")
    all_new_lines: set[str] = set()
    for variant in [PT_MZ, PT_AO]:
        all_new_lines.update(iterate_over_african_dictionary(variant, pt_lemmata))
    print(f"Final number of lemmata: {len(pt_lemmata)}")
    print(f"Number of new lines: {len(all_new_lines)}")
    with open(PT_PT.dic(), 'a', encoding="ISO-8859-1") as pt_dic_file:
        pt_dic_file.write("\n".join(all_new_lines))


if __name__ == '__main__':
    main()
