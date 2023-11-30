from pt_dict.variants.alternation import Transformation, AlternationContext, Alternation
from pt_dict.variants.syllabifier import Syllabifier


class TestAlternation:
    syllabifier = Syllabifier()

    def test_transformation(self):
        transformation = Transformation('foo', 'bar')
        assert 'foo=bar' == transformation.__str__()

    def test_alternation_context_contains(self):
        contexts = [
            ('x', 'ex', True),
            ('x', 'ez', False)
        ]
        for grapheme, word, result in contexts:
            assert AlternationContext(grapheme, 'contains').applies_to(self.syllabifier.syllabify(word)) is result

    def test_alternation_context_whole(self):
        contexts = [
            ('x', 'ex', False),
            ('x', 'x', True)
        ]
        for grapheme, word, result in contexts:
            assert AlternationContext(grapheme, 'whole').applies_to(self.syllabifier.syllabify(word)) is result

    def test_alternation_context_vowel(self):
        contexts = [
            ('ê', 'tênis', True),
            ('ô', 'ônus', True),
            ('ô', 'bom', False),
            ('ô', 'harmônicas', True),
            ('ê', 'consequência', False),
            ('ô', 'Rondônia', True),
            ('ê', 'bebê', True)
        ]
        for grapheme, word, result in contexts:
            assert AlternationContext(grapheme, 'vowel').applies_to(self.syllabifier.syllabify(word)) is result

    def test_alternation(self):
        context = AlternationContext('ê', 'vowel')
        alternation = Alternation(context, 'é', ['pavê'])
        alternation.transform(self.syllabifier.syllabify('consequência'))  # context does not apply
        assert len(alternation.transformations) == 0
        alternation.transform(self.syllabifier.syllabify('pavê'))  # exception
        assert len(alternation.transformations) == 0
        alternation.transform(self.syllabifier.syllabify('armênio'))  # context applies
        assert len(alternation.transformations) == 1
        assert alternation.transformations[0].target == 'arménio'
