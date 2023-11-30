from typing import List
import re

from pt_dict.variants.syllabifier import Syllabifier, Syllable


class TestSyllabifier:
    def test_syllable_ends_with(self):
        assert Syllable('a').endswith('a')
        assert Syllable('ba').endswith('[ae]')

    def test_syllable_startswith(self):
        assert Syllable('a').startswith('a')
        assert Syllable('ab').startswith('[ac]')

    def test_syllable_is_accented(self):
        assert Syllable('a').is_accented() is False
        assert Syllable('é').is_accented() is True

    def test_syllabifier_hiatus(self):
        assert Syllabifier().is_hiatus(Syllable('a'), Syllable('o'))

    def test_syllable_letter(self):
        assert Syllable('abc').letter(0) == 'a'
        assert Syllable('abc').letter(-1) == 'c'
        assert Syllable('abc').letter(5) is None

    def test_syllable_valid_rising_diphthong(self):
        assert Syllable('iam').is_valid_rising_diphthong() is True
        assert Syllable('rie').is_valid_rising_diphthong() is True
        assert Syllable('gua').is_valid_rising_diphthong() is False

    def test_syllable_sub(self):
        syl = Syllable('foo')
        syl.sub(re.compile('f'), 'z')
        assert syl.value == 'zoo'

    def test_syllable_to_hiatus(self):
        syl = Syllable('ia')
        hiatus = syl.to_hiatus()
        assert isinstance(hiatus, List)
        assert isinstance(hiatus[0], Syllable)
        assert hiatus[0].value == 'i'
        assert hiatus[1].value == 'a'
        assert Syllable('baú').to_hiatus()[1].value == 'ú'

    def test_syllabifier(self):
        syllabifier = Syllabifier()
        syllabifications = [
            ('água', ['á', 'gua']),
            ('tênis', ['tê', 'nis']),
            ('ônus', ['ô', 'nus']),
            ('hora', ['ho', 'ra']),
            ('consequência', ['con', 'se', 'quên', 'cia']),
            ('ênfase', ['ên', 'fa', 'se']),
            ('fria', ['fri', 'a']),
            ('ironia', ['i', 'ro', 'ni', 'a']),
            ('iam', ['i', 'am']),
            ('séries', ['sé', 'ries']),
            ('judiar', ['ju', 'di', 'ar']),
            ('órgão', ['ór', 'gão']),
            ('consciência', ['cons', 'ciên', 'cia']),
            ('consciente', ['cons', 'ci', 'en', 'te']),
            ('wolfrâmio', ['wol', 'frâ', 'mio']),
            ('iguaria', ['i', 'gua', 'ri', 'a']),
            ('armário', ['ar', 'má', 'rio']),
            ('baia', ['bai', 'a']),
            ("olho-d'água", ['o', 'lho', 'dá', 'gua']),
            # these are *not* syllabified the way they should be, but for now we don't *need* them to be
            ('baía', ['ba', 'ía']),
            ('baú', ['baú']),
        ]
        for word, syllables in syllabifications:
            assert [syl.value for syl in syllabifier.syllabify(word).values] == syllables
