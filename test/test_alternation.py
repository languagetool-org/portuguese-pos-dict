from variants.alternation import Transformation, AlternationContext, Alternation
from variants.syllabifier import Syllabifier


class TestAlternation:
    def test_transformation(self):
        transformation = Transformation('foo', 'bar')
        assert 'foo=bar' == transformation.__str__()

    def test_alternation_context_contains(self):
        contexts = [
            ('x', 'ex', True),
            ('x', 'ez', False)
        ]
        for context in contexts:
            assert AlternationContext(context[0], 'contains', Syllabifier()).applies_to(context[1]) is context[2]

    def test_alternation_context_whole(self):
        contexts = [
            ('x', 'ex', False),
            ('x', 'x', True)
        ]
        for context in contexts:
            assert AlternationContext(context[0], 'whole', Syllabifier()).applies_to(context[1]) is context[2]

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
        for context in contexts:
            assert AlternationContext(context[0], 'vowel', Syllabifier()).applies_to(context[1]) is context[2]

    def test_alternation(self):
        context = AlternationContext('ê', 'vowel', Syllabifier())
        alternation = Alternation(context, 'é', ['pavê'])
        alternation.transform('consequência')  # context does not apply
        assert len(alternation.transformations) == 0
        alternation.transform('pavê')  # exception
        assert len(alternation.transformations) == 0
        alternation.transform('armênio')  # context applies
        assert len(alternation.transformations) == 1
        assert alternation.transformations[0].target == 'arménio'

