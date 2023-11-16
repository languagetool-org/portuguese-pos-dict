"""This script is meant to migrate words from the Hunspell source dictionary to the tagger dictionary. We need to apply
some kind of heuristics to determine the POS."""
import re

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict
from pt_dict.utils import print_sample
from pt_dict.variants.variant import Variant, PT_BR, PT_PT_90


def collect_tagged_lemmata(variant: Variant):
    tag_pattern = re.compile("^([^/\\t#]+)(?:/([\\w]+))?$")
    untagged_all = set()
    untagged_proper = set()
    tagged = set()
    with open(variant.dic(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
        for line in dic_file.read().split('\n'):
            match = tag_pattern.match(line)
            if match:
                if match.group(2):
                    tagged.add((match.group(1), match.group(2)))
                else:
                    lemma = match.group(1)
                    if re.compile("^[A-ZÂÁÃÉÊÍÓÔÕÚÇ][a-zâáãéêíóôõú]+").match(lemma):
                        untagged_proper.add(lemma)
                    else:
                        untagged_all.add(lemma)
    print(f"total tagged: {len(set([lemma for lemma, tag in tagged]).difference(TAGGER_LEMMATA))}")
    print_sample([':'.join(pair) for pair in tagged], 10)
    print(f"total untagged: {len(untagged_all.union(untagged_proper).difference(TAGGER_LEMMATA))}")
    print_sample(list(untagged_all.difference(TAGGER_LEMMATA)), 10)
    print_sample(list(untagged_proper.difference(TAGGER_LEMMATA)), 10)


def main():
    for var in [PT_BR]:
        collect_tagged_lemmata(var)


if __name__ == '__main__':
    TAGGER_LEMMATA = TaggerDict().collect_lemmata()
    main()
