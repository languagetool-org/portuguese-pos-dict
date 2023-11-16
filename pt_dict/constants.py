import logging
from os import path, environ
import pathlib

from pt_dict.logger import Logger

LT_VER = "6.4-SNAPSHOT"
LATIN_1_ENCODING = 'ISO-8859-1'

# Paths
REPO_DIR = pathlib.Path(path.dirname(path.abspath(__file__))).parent
LT_HOME = environ.get('LT_HOME')
LT_DIR = path.join(pathlib.Path(REPO_DIR).parent, "languagetool") if LT_HOME is None else LT_HOME
RESOURCE_DIR = path.join(LT_DIR, "languagetool-language-modules/pt/src/main/resources/org/languagetool/resource/pt")
RULES_DIR = path.join(LT_DIR, "languagetool-language-modules/pt/src/main/resources/org/languagetool/rules/pt")
DATA_DIR = path.join(REPO_DIR, 'data')
DICT_DIR = path.join(DATA_DIR, "spelling-dict")
HUNSPELL_DIR = path.join(DICT_DIR, "hunspell")
TAGGER_DICT_DIR = path.join(DATA_DIR, "src-dict")
SYLLABLES_FILEPATH = path.join(DATA_DIR, 'syllables.tsv')
ALTERNATIONS_DIR = path.join(DATA_DIR, 'alternations')
PT_BR_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_br.txt')
SILENT_LETTER_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'silent_letters.tsv')
PT_45_90_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_45_90.tsv')
COMPOUNDS_FILEPATH = path.join(RESOURCE_DIR, "post-reform-compounds.txt")
COMPOUNDS_DIR = path.join(DATA_DIR, 'compounds')

RESULTS_DIR = path.join(REPO_DIR, 'results', 'java-lt')
OUTPUT_DIR = path.join(RESULTS_DIR, "src/main/resources/org/languagetool/resource/pt/spelling")
LT_JAR_PATH = path.join(LT_DIR, 'languagetool-standalone', 'target', f"LanguageTool-{LT_VER}", f"LanguageTool-{LT_VER}",
                        'languagetool.jar')
LT_JAR_WITH_DEPS_PATH = path.join(LT_DIR, "languagetool-dev", "target",
                                  f"languagetool-dev-{LT_VER}-jar-with-dependencies.jar")

logging.setLoggerClass(Logger)
LOGGER = logging.getLogger('build_spelling_dicts')
LOGGER.setLevel(logging.DEBUG)
