"""Extract differences between PT varieties."""
import argparse
import concurrent.futures
import logging
from copy import deepcopy
from typing import List, Optional

import numpy

from pt_dict.constants import SYLLABLES_FILEPATH, TWO_WAY_ALTERNATIONS_FILEPATH
from pt_dict.utils import get_source_dict
from pt_dict.variants.syllabifier import SyllabifierException, SyllablesFile
from pt_dict.variants.alternation import AlternationContext, Alternation, Transformation

ALTERNATIONS = [
    Alternation(AlternationContext('ê', 'vowel'), 'é', []),
    Alternation(AlternationContext('ô', 'vowel'), 'ó', []),
    # Alternation(AlternationContext('pt', 'contains', SYLLABIFIER), 't', []),
    # Alternation(AlternationContext('cç', 'contains', SYLLABIFIER), 'ç', []),
    # Alternation(AlternationContext('ct', 'contains', SYLLABIFIER), 't', []),
    # Alternation(AlternationContext('pç', 'contains', SYLLABIFIER), 'ç', []),
]


class CLI:
    """Class to handle the command line interface of this script."""
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--source', type=str, choices=['hunspell', 'tagger'], default='hunspell',
                                 help="Which lexicon to take as source (hunspell or tagger).")
        self.parser.add_argument('--threads', type=int, default=8,
                                 help="Number of concurrent threads to use.")
        self.parser.add_argument('--syllables', type=str, default=SYLLABLES_FILEPATH,
                                 help=f"Location of the syllables file (default: {SYLLABLES_FILEPATH}")
        self.args = self.parser.parse_args()


def merge_transformations(transformations: List[Transformation]) -> Optional[Transformation]:
    """Given a list of transformations, essentially zip their source and target words and combine them."""
    compound_source = []
    compound_target = []
    for partial_transformation in transformations:
        compound_source.append(partial_transformation.source)
        compound_target.append(partial_transformation.target)
    merged_source = '-'.join(compound_source)
    merged_target = '-'.join(compound_target)
    # Only return a transformation if source and target actually differ!
    if merged_source != merged_target:
        return Transformation(merged_source, merged_target)


def process_lemma_chunk(lemma_chunk: numpy.array, syllables_file: SyllablesFile) -> List[Transformation]:
    """For each lemma in a chunk, create a transformation based on each of the alternations.

    Since alternations work **per word** (as they depend on the syllabification and accentuation pattern), we must
    split each lemma into its constituent parts. For most lemmata, that'll be straightforward, but for **compounds**,
    we need to split them on every hyphen.

    Once split, we must see if an alternation context applies to each individual part of the compound. If it does,
    great, but if it doesn't, we must create a dummy transformation with identical source and target words, because a
    later part of the compound might still have a valid transformation.

    For example:
        lemma: podômetro-pé
        parts: [podômetro, pé]
        transformations: [podómetro, None => pé]
        merged as: podômetro-pé=podómetro-pé
    """
    transformations: List[Transformation] = []
    for lemma in lemma_chunk:
        lemma = str(lemma)
        for alternation in ALTERNATIONS:
            alternation = deepcopy(alternation)  # for thread-safety
            compound_parts = lemma.split('-')
            compound_transformations: List[Transformation] = []
            for compound_part in compound_parts:
                try:
                    # the syllables file should contain syllabification for each individual part of every compound
                    syllables = syllables_file.syllable_from_word(compound_part)
                    if syllables is not None:  # we found a syllabification for this word
                        compound_transformation = alternation.transform(syllables)
                        if compound_transformation:  # if the transformation is valid
                            compound_transformations.append(alternation.transform(syllables))
                        # the transformation is not valid (returns None), but we're dealing with a compound
                        elif len(compound_parts) > 1:
                            compound_transformations.append(Transformation(compound_part, compound_part))
                    else:  # no syllabification found
                        logging.warning(f"Could not find syllabification for \"{lemma}\". Skipping.")
                        break
                except SyllabifierException as e:
                    logging.warning(f"{e} Skip.")
                    break
                if len(compound_transformations) != len(compound_parts):
                    break
            merged_transformation = merge_transformations(compound_transformations)
            if merged_transformation:
                transformations.append(merged_transformation)
    return transformations


def main():
    cli = CLI()  # construct CLI
    source_lemmata = get_source_dict(cli.args.source).collect_lemmata(split_compounds=False)
    # source_lemmata = set(list(source_lemmata)[0:1000])
    max_threads = cli.args.threads
    lemma_chunks = numpy.array_split(numpy.array(list(source_lemmata)), max_threads)
    syllables_files = SyllablesFile(cli.args.syllables)
    syllables_files.read()
    all_transformations: List[Transformation] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda chunk: process_lemma_chunk(chunk, syllables_files), lemma_chunks)
        for result in results:
            all_transformations.extend(result)
    # TODO: for now, we only have BR=PT alternations, but later we will also have PT_PRE/PT_POST alternations
    with open(TWO_WAY_ALTERNATIONS_FILEPATH, 'a', encoding='utf-8') as output_file:
        output_file.write("\n".join([transformation.__str__() for transformation in all_transformations]))
        output_file.write("\n")


if __name__ == '__main__':
    main()
