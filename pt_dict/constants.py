import logging
from os import path, environ
import pathlib

from pt_dict.logger import Logger

LT_VER = "6.4-SNAPSHOT"

# Paths
REPO_DIR = pathlib.Path(path.dirname(path.abspath(__file__))).parent
LT_HOME = environ.get('LT_HOME')
LT_DIR = path.join(pathlib.Path(REPO_DIR).parent, "languagetool") if LT_HOME is None else LT_HOME
OUTPUT_DIR = path.join(REPO_DIR, "results/java-lt/src/main/resources/org/languagetool/resource/pt/spelling")
DATA_DIR = path.join(REPO_DIR, 'data')
DICT_DIR = path.join(DATA_DIR, "spelling-dict")
HUNSPELL_DIR = path.join(DICT_DIR, "hunspell")
TAGGER_DICT_DIR = path.join(DATA_DIR, "src-dict")
SYLLABLES_FILEPATH = path.join(DATA_DIR, 'syllables.tsv')
TWO_WAY_ALTERNATIONS_FILEPATH = path.join(DATA_DIR, 'two-way-alternations.txt')
THREE_WAY_ALTERNATIONS_FILEPATH = path.join(DATA_DIR, 'three-way-alternations.txt')
LT_JAR_PATH = path.join(LT_DIR, 'languagetool-standalone', 'target', f"LanguageTool-{LT_VER}", f"LanguageTool-{LT_VER}",
                        'languagetool.jar')

logging.setLoggerClass(Logger)
LOGGER = logging.getLogger('build_spelling_dicts')
LOGGER.setLevel(logging.DEBUG)
