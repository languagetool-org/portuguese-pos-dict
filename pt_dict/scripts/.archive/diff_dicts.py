from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict
from pt_dict.utils import print_sample

if __name__ == "__main__":
    SAMPLE_SIZE = 100

    tagger_lemmata = TaggerDict().collect_lemmata()
    hunspell_lemmata = HunspellDict().collect_lemmata()

    all_lemmata = hunspell_lemmata.union(tagger_lemmata)
    common_lemmata = hunspell_lemmata.intersection(tagger_lemmata)
    different_lemmata = tagger_lemmata.symmetric_difference(hunspell_lemmata)
    hunspell_only_lemmata = hunspell_lemmata.difference(tagger_lemmata)
    tagger_only_lemmata = tagger_lemmata.difference(hunspell_lemmata)

    print('total lemmata:', len(all_lemmata))
    print('total lemmata from tagger dict:', len(tagger_lemmata))
    print('total lemmata from hunspell:', len(hunspell_lemmata))
    print('lemmata in common:', len(common_lemmata))
    print('different lemmata between both:', len(different_lemmata))
    print('hunspell-only lemmata:', len(hunspell_only_lemmata))
    print('tagger-only lemmata:', len(tagger_only_lemmata))
    print_sample(list(tagger_only_lemmata), SAMPLE_SIZE)
