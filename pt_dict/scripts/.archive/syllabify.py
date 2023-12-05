"""This script is here to generate a list of syllabified lemmata.

The output file for this script is located in /data/syllabified.tsv, and it is a tab-separated file where the first
column is the unsyllabified source form of the word, and the second column is its syllabification.

This is done so as to bootstrap the process of creating dialectal variation, since, in order to do that, we need
information about syllables.

Note that, crucially, we split source words by hyphens. That is because compounds should be syllabified separately.
This makes the process faster (we don't need to keep re-syllabifying 'foofoo-de-fafa') as well as makes it possible to
syllabify individual components of the same compound. For example, the nonce compound 'podómetro-pé' would *not* be
converted into 'podômetro-pé', because the syllables don't line up.
"""

import argparse
import concurrent.futures
import logging
from typing import List
import numpy

from pt_dict.constants import SYLLABLES_FILEPATH
from pt_dict.utils import get_source_dict
from pt_dict.variants.syllabifier import Syllabifier, SyllabifierException, Syllables, SyllablesFile


class CLI:
    """Class to handle the command line interface of this script."""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--source', type=str, choices=['hunspell', 'tagger'], default='hunspell',
                                 help="Which lexicon to take as source (hunspell or tagger).")
        self.parser.add_argument('--threads', type=int, default=8,
                                 help="Number of concurrent threads to use.")
        self.parser.add_argument('--force', type=bool, default=False,
                                 help="Whether to overwrite existing syllabifications or only update the file. May be "
                                      "useful if we ever update the syllabification logic.")
        self.parser.add_argument('--output', type=str, default=SYLLABLES_FILEPATH,
                                 help=f"Location to save the syllables file (default: {SYLLABLES_FILEPATH}")
        self.args = self.parser.parse_args()


def syllabify_lemmata(lemmata, syllables_file: SyllablesFile) -> List[Syllables]:
    """Given a list of lemmata, syllabify each of them and return a list of Syllables objects."""
    logging.debug(f"starting syllabification of {len(lemmata)} lemmata")
    syllables: List[Syllables] = []
    for lemma in lemmata:
        lemma = str(lemma)
        # TODO: those containing '.' are mostly abbreviations and we can't syllabify them properly anyway, but spaCy
        # still tries... move this logic somewhere else
        if not syllables_file.contains(lemma) and '.' not in lemma and lemma != '':
            try:
                syllables.append(Syllabifier.syllabify(lemma))
            except SyllabifierException as e:
                logging.warning(f"{e} Skipping.")
    logging.debug('total syllables for chunk:', len(syllables))
    return syllables


def main():
    cli = CLI()  # construct CLI
    source_lemmata = get_source_dict(cli.args.source).collect_lemmata(split_compounds=True)
    logging.debug('total lemmata:', len(source_lemmata))
    max_threads = cli.args.threads
    lemmata_chunks = numpy.array_split(numpy.array(list(source_lemmata)), max_threads)
    logging.debug('chunk sizes:', [len(chunk) for chunk in lemmata_chunks])
    syllables_file = SyllablesFile(cli.args.output)
    # Skip getting current words if we want to force overwrite of the whole file.
    if not cli.args.force:
        syllables_file.read()
    all_syllables: List[Syllables] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda chunk: syllabify_lemmata(chunk, syllables_file), lemmata_chunks)
        for result in results:
            all_syllables.extend(result)
    logging.debug("total syllables:", len(all_syllables))
    syllables_file.write(all_syllables, force_overwrite=cli.args.force)


if __name__ == "__main__":
    main()
