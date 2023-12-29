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
SPELLING_DICT_DIR = path.join(DATA_DIR, "spelling-dict")
HUNSPELL_DIR = path.join(SPELLING_DICT_DIR, "hunspell")
TAGGER_DICT_DIR = path.join(DATA_DIR, "src-dict")
TAGGER_SCRIPTS_DIR = path.join(REPO_DIR, "pos_tagger_scripts")
TAGGER_BUILD_SCRIPT_PATH = path.join(TAGGER_SCRIPTS_DIR, "build-lt.sh")
SYLLABLES_FILEPATH = path.join(DATA_DIR, 'misc', 'syllables.tsv')
ALTERNATIONS_DIR = path.join(DATA_DIR, 'alternations')
PT_BR_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_br.txt')
SILENT_LETTER_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'silent_letters.tsv')
PT_45_90_ALTERNATIONS_FILEPATH = path.join(ALTERNATIONS_DIR, 'pt_45_90.tsv')
COMPOUNDS_FILEPATH = path.join(RESOURCE_DIR, "post-reform-compounds.txt")
COMPOUNDS_DIR = path.join(HUNSPELL_DIR, 'compounds')
TO_ADD_DIR = path.join(DATA_DIR, "to_add")

RESULTS_DIR = path.join(REPO_DIR, 'results')
JAVA_RESULTS_DIR = path.join(RESULTS_DIR, 'java-lt')
LT_RESULTS_DIR = path.join(RESULTS_DIR, 'lt')
FDIC_DIR = path.join(TAGGER_SCRIPTS_DIR, "fdic-to-lt")
RESULT_POS_DICT_FILEPATH = path.join(LT_RESULTS_DIR, "dict.txt")
SORTED_POS_DICT_FILEPATH = path.join(LT_RESULTS_DIR, "dict_sorted.txt")
POS_DICT_DIFF_FILEPATH = path.join(LT_RESULTS_DIR, "dict.diff")
OLD_POS_DICT_FILEPATH = path.join(LT_RESULTS_DIR, "dict.old")
COMPILED_POS_DICT_FILEPATH = path.join(JAVA_RESULTS_DIR, )
JAVA_OUTPUT_DIR = path.join(JAVA_RESULTS_DIR, "src/main/resources/org/languagetool/resource/pt")
SPELLING_OUTPUT_DIR = path.join(JAVA_OUTPUT_DIR, "spelling")
POS_DICT_JAVA_OUTPUT_PATH = path.join(JAVA_OUTPUT_DIR, "portuguese.dict")
POS_INFO_JAVA_INPUT_PATH = path.join(TAGGER_DICT_DIR, "portuguese.info")
POS_INFO_JAVA_OUTPUT_PATH = path.join(JAVA_OUTPUT_DIR, "portuguese.info")
SYNTH_DICT_JAVA_OUTPUT_PATH = path.join(JAVA_OUTPUT_DIR, "portuguese_synth.dict")
SYNTH_INFO_JAVA_OUTPUT_PATH = path.join(JAVA_OUTPUT_DIR, "portuguese_synth.info")
SYNTH_INFO_JAVA_INPUT_PATH = path.join(TAGGER_DICT_DIR, "portuguese_synth.info")
LT_JAR_PATH = path.join(LT_DIR, 'languagetool-standalone', 'target', f"LanguageTool-{LT_VER}", f"LanguageTool-{LT_VER}",
                        'languagetool.jar')
LT_JAR_WITH_DEPS_PATH = path.join(LT_DIR, "languagetool-dev", "target",
                                  f"languagetool-dev-{LT_VER}-jar-with-dependencies.jar")

logging.setLoggerClass(Logger)
LOGGER = logging.getLogger('build_spelling_dicts')
LOGGER.setLevel(logging.DEBUG)
