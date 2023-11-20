import re
from os import path
from typing import Callable

from pt_dict.constants import TO_ADD_DIR, LATIN_1_ENCODING
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import PT_BR, PT_PT_90, PT_PT_45, Variant


def do_nothing(word: str) -> str:
    return word


def oa_normaliser(word: str) -> str:
    return re.compile('[oa]s?$').sub('o', word)


def number_normaliser(word: str) -> str:
    return re.compile('s?$').sub('', word)


def tag_word(word: str, tags: str) -> str:
    if tags == '':
        return word
    return f"{word}/{tags}"


def tag_words(words: set[str], tags: str) -> set[str]:
    return set([f"{tag_word(word, tags)}" for word in words])


def new_lookup(br_tags: str, pt_tags: str) -> dict:
    return {
        'pt-BR-90': {
            'tags': br_tags,
            'new_words': set()
        },
        'pt-PT-90': {
            'tags': pt_tags,
            'new_words': set()
        },
        'pt-PT-45': {
            'tags': pt_tags,
            'new_words': set()
        }
    }


def collect_words_from_file(filepath: str, normaliser: Callable) -> set[str]:
    words = set()
    with open(filepath, 'r') as file:
        lines = file.read().split("\n")
        for line in lines:
            if line.startswith("#") or line == '':
                continue
            words.add(normaliser(line.strip()))
    return words


def add_word(word: str, variant: Variant, lookup: dict):
    if word not in LEMMATA[variant.hyphenated_with_agreement]:
        lookup[variant.hyphenated_with_agreement]['new_words'].add(word)


def clean_file(filename: str, br_tags: str, pt_tags: str, normaliser: Callable):
    print(filename)
    filepath = path.join(TO_ADD_DIR, filename)
    lookup = new_lookup(br_tags, pt_tags)
    words = collect_words_from_file(filepath, normaliser)
    for variant in VARIANTS:
        for word in words:
            add_word(word, variant, lookup)

        new_words = lookup[variant.hyphenated_with_agreement]['new_words']
        tags = lookup[variant.hyphenated_with_agreement]['tags']
        print(f"{variant.hyphenated_with_agreement}: {len(new_words)}")
        tagged = tag_words(new_words, tags)
        print("\n".join(tagged))
        if not DRY_RUN:
            add_to_dic(tagged, variant)


def add_to_dic(words: set[str], variant: Variant):
    lines = []
    with open(variant.dic(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
        lines.extend(dic_file.read().split("\n")[1:])
    lines.extend(words)  # preserve order
    with open(variant.dic(), 'w', encoding=LATIN_1_ENCODING) as dic_file:
        dic_file.write(str(len(lines)) + "\n")
        dic_file.write("\n".join(lines))


def clean_able():
    def normaliser(w: str) -> str:
        if w.endswith("is"):
            return w[:-2] + 'l'
        return w
    clean_file('able.txt', 'KXIB', 'pms', normaliser)


def clean_ador():
    def normaliser(w: str) -> str:
        return re.compile('([aei]dor)(es|as?)?$').sub(r"\1", w)
    clean_file('ador.txt', 'DR', 'fp', normaliser)


def clean_adverbs():
    clean_file('adverbs.txt', '', '', do_nothing)


def clean_orio():
    clean_file('orio.txt', 'D', 'fp', oa_normaliser)


def clean_logy():
    def normaliser(w: str) -> str:
        return re.compile('s?$').sub('', w)
    clean_file('logy.txt', 'B', 'p', normaliser)


def clean_logue():
    clean_file('logue.txt', 'D', 'fp', oa_normaliser)


def clean_metry():
    def normaliser(w: str) -> str:
        return re.compile('s?$').sub('', w)
    clean_file('metria.txt', 'B', 'p', normaliser)


def clean_eiro():
    clean_file('eiro_ario.txt', 'D', 'fp', oa_normaliser)


def clean_suffixed_nouns():
    def normaliser(w: str) -> str:
        if w.endswith('ões'):
            return w[:-3] + 'ão'
        if w.endswith('ns'):
            return w[:-2] + 'm'
        return re.compile('([oae])s?$').sub(r"\1", w)
    clean_file('suffixed_nouns.txt', 'B', 'p', normaliser)


def clean_adj_e():
    def normaliser(w: str) -> str:
        return re.compile('s?$').sub('', w)
    clean_file('adj_e.txt', 'B', 'p', normaliser)


def clean_adj_oa():
    clean_file('adj_oa.txt', 'D', 'fp', oa_normaliser)


def clean_ito():
    clean_file('ito.txt', 'D', 'fp', oa_normaliser)


def clean_weirdcase():
    clean_file('weirdcase.txt', '', '', do_nothing)


def clean_diminutives():
    clean_file("diminutives.txt", "B", "p", number_normaliser)


def clean_eiro_proper():
    clean_file("eiro_proper.txt", '', '', do_nothing)


def clean_initialisms():
    clean_file("initialisms.txt", '', '', do_nothing)


def clean_ano():
    clean_file("ano.txt", 'D', 'fp', oa_normaliser)


def clean_gender_number():
    clean_file("gender_number.txt", 'D', 'fp', oa_normaliser)


def clean_verbs_ar():
    clean_file("verbs_ar.txt", 'akYL', 'ZYL', do_nothing)


def clean_verbs_ir():
    clean_file("verbs_ir.txt", 'cmL', 'KPL', do_nothing)


def clean_verbs_er():
    clean_file("verbs_er.txt", 'XPL', 'XPL', do_nothing)


def write_to_txt(filename: str, words: set[str]):
    print(f"{filename}: {len(words)}")
    filepath = path.join(TO_ADD_DIR, filename)
    with open(filepath, 'w') as file:
        file.write("\n".join(sorted(words)))


def sort_added():
    filepath = path.join(TO_ADD_DIR, 'added.txt')
    all_words = collect_words_from_file(filepath, do_nothing)
    all_words_final = all_words.copy()
    gender_number_words = set()
    number_words = set()
    for word in all_words:
        if re.compile('[^oa]s$').search(word):
            normalised = word[:-1]
            naive_normalised = normalised
            if word.endswith('ns'):
                normalised = word[:-2] + 'm'
            elif re.compile('[aeou]is$').search(word):
                normalised = word[:-2] + 'l'
            elif word.endswith('res'):
                normalised = word[:-2]
            elif word.endswith('ões') or word.endswith('ães') or word.endswith('ãos'):
                normalised = word[:-3] + 'ão'
            elif word.endswith('óis'):
                normalised = word[:-3] + 'ol'
            elif word.endswith('éis'):
                normalised = word[:-3] + 'el'
            if normalised in all_words:
                number_words.add(normalised)
                all_words_final.discard(word)
                all_words_final.discard(normalised)
            elif naive_normalised in all_words:
                number_words.add(naive_normalised)
                all_words_final.discard(word)
                all_words_final.discard(naive_normalised)
        if re.compile('as$').search(word):
            masc_sg = word[:-2] + 'o'
            fem_sg = word[:-1]
            if masc_sg in all_words:
                gender_number_words.add(masc_sg)
                all_words_final.discard(word)  # fem_pl
                all_words_final.discard(masc_sg)
                all_words_final.discard(fem_sg)  # fem_sg
                all_words_final.discard(masc_sg + 's')  # masc_pl
            elif fem_sg in all_words:
                number_words.add(fem_sg)
                all_words_final.discard(word)  # fem_pl
                all_words_final.discard(fem_sg)
        if re.compile('os$').search(word):
            masc_sg = word[:-1]
            fem_sg = masc_sg[:-1] + 'a'
            if masc_sg in all_words and fem_sg not in all_words:
                number_words.add(masc_sg)
                all_words_final.discard(word)  # masc_pl
                all_words_final.discard(masc_sg)
    print("starting point:", len(all_words))
    write_to_txt("added_clean.txt", all_words_final)
    write_to_txt("number_only.txt", number_words)
    write_to_txt("gender_number.txt", gender_number_words)


if __name__ == "__main__":
    VARIANTS = [PT_BR, PT_PT_90, PT_PT_45]
    br_dict = Dictionary()
    pt_90_dict = Dictionary()
    pt_45_dict = Dictionary()
    br_dict.collect_lemmata_from_file(PT_BR.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    pt_90_dict.collect_lemmata_from_file(PT_PT_90.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    pt_45_dict.collect_lemmata_from_file(PT_PT_45.dic(), HunspellDict.pattern, encoding=LATIN_1_ENCODING, offset=1)
    LEMMATA = {
        'pt-BR-90': br_dict.lemmata,
        'pt-PT-90': pt_90_dict.lemmata,
        'pt-PT-45': pt_45_dict.lemmata
    }
    DRY_RUN = False

    # sort_added()

    # clean_able()
    # clean_ador()
    # clean_adverbs()
    # clean_orio()
    # clean_logy()
    # clean_logue()
    # clean_metry()
    # clean_eiro()
    # clean_suffixed_nouns()
    # clean_adj_e()
    # clean_adj_oa()
    # clean_weirdcase()
    # clean_ito()
    # clean_diminutives()
    # clean_eiro_proper()
    # clean_initialisms()
    # clean_ano()
    # clean_gender_number()
    # clean_verbs_ar()
    # clean_verbs_ir()
    clean_verbs_er()
