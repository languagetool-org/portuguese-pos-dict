"""In this module we define the logic for alternations between variants."""
from typing import Literal, Optional, List

from pt_dict.variants.syllabifier import Syllables
import pt_dict.variants.phonology as phon


class Transformation:
    """A single word-wise transformation, from one lemma to another."""
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def __str__(self) -> str:
        return "=".join([self.source, self.target])


class AlternationContext:
    """This class defines the context where an alternation applies.

    Attributes:
        core: the meaningful/variable component of the alternation, usually a grapheme or digraph;
        type: defines how the context is constructed; 'contains' refers to a simple contains, every instance of `core`
              is uncritically replaced; 'whole' means that only when the whole word matches 'core' do we apply the
              alternation; 'vowel' means we need some more complex logic for the open/closed vowel alternations
    """

    def __init__(self, core: str, alternation_type: Literal['contains', 'whole', 'vowel']):
        self.type = alternation_type
        self.core = core

    def applies_to(self, syllables: Syllables) -> bool:
        """Return True if the alternation context applies to a given natural language (nl) string, usually a word."""
        if self.type == 'contains' and self.core in syllables.word:
            return True
        if self.type == 'whole' and self.core == syllables.word:
            return True
        if self.type == 'vowel':
            # check tê.nis/té.nis OR Ron.dô.nia/Ron.dó.nia
            if syllables.penultimate and syllables.penultimate.endswith(self.core) and \
                    (syllables.last.endswith(f"{phon.UNDERLYING_STRESSED_VOWELS}s?") or
                     syllables.last.is_valid_rising_diphthong()):
                return True
            # check har.mô.ni.co/har.mó.ni.co
            if syllables.antepenultimate and syllables.antepenultimate.contains(self.core) and \
                    syllables.penultimate.startswith(phon.NASALS):
                return True
            # check be.bê/be.bé; too many false positives, switching this off, but leaving it here for now just in case
            # if syllables.last.endswith(self.core):
            #     return True
        return False


class Alternation:
    """The phenomenon of lexical alternation writ large.

    Attributes:
        source: the source grapheme or digraph
        target: the target grapheme or digraph
        context: the context in which an alternation is valid
        exceptions: a set of words extracted from the file that exceptions_filepath points to
        transformations: a set of transformations, i.e. source=target lemma pairs
    """
    def __init__(self, context: AlternationContext, target: str, exceptions=List[str]):
        self.context = context
        self.source = self.context.core
        self.target = target
        self.exceptions = set(exceptions)
        self.transformations: List[Transformation] = []

    def transform(self, syllables: Syllables) -> Optional[Transformation]:
        if syllables.word in self.exceptions:
            return
        if self.context.applies_to(syllables):
            transformed_word = syllables.word.replace(self.source, self.target)
            transformation = Transformation(syllables.word, transformed_word)
            self.transformations.append(transformation)
            return transformation
