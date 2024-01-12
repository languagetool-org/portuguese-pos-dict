from os import path
import pathlib

from dict_tools.lib.constants import DATA_DIR

# Paths
PT_REPO_DIR = pathlib.Path(path.dirname(path.abspath(__file__))).parent
SYLLABLES_FILEPATH = path.join(DATA_DIR, 'misc', 'syllables.tsv')
ALTERNATIONS_DIR = path.join(DATA_DIR, 'alternations')
PT_BR_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_br.txt')
SILENT_LETTER_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'silent_letters.tsv')
PT_45_90_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_45_90.tsv')
TO_ADD_DIR = path.join(DATA_DIR, "to_add")
