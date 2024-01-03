"""This script builds the binaries for the tagger and synthesiser dictionaries. It has much less in terms of specific
logic, since most of it remains written in Perl.
"""
import os
import shutil
from os import path

from pt_dict.constants import TAGGER_BUILD_SCRIPT_PATH, FDIC_DIR, RESULT_POS_DICT_FILEPATH, SORTED_POS_DICT_FILEPATH, \
    POS_DICT_DIFF_FILEPATH, OLD_POS_DICT_FILEPATH, POS_DICT_JAVA_OUTPUT_PATH, POS_INFO_JAVA_OUTPUT_PATH, \
    POS_INFO_JAVA_INPUT_PATH, SYNTH_DICT_JAVA_OUTPUT_PATH, SYNTH_INFO_JAVA_OUTPUT_PATH, SYNTH_INFO_JAVA_INPUT_PATH, \
    REPO_DIR, TAGGER_DICT_DIR, LT_RESULTS_DIR, LT_JAR_PATH, JAVA_OUTPUT_DIR
from pt_dict.utils import run_command_with_output, run_command, compile_lt_dev


def set_shell_env() -> dict[str, str]:
    custom_env = {
        'REPO_DIR': REPO_DIR,
        'DATA_SRC_DIR': TAGGER_DICT_DIR,
        'RESULTS_DIR': LT_RESULTS_DIR,
        'FDIC_DIR': FDIC_DIR,
        'RESULT_DICT_FILEPATH': RESULT_POS_DICT_FILEPATH,
        'SORTED_DICT_FILEPATH': SORTED_POS_DICT_FILEPATH,
        'DICT_DIFF_FILEPATH': POS_DICT_DIFF_FILEPATH,
        'OLD_DICT_FILEPATH': OLD_POS_DICT_FILEPATH
    }
    return {**os.environ, **custom_env}


def run_shell_script(env: dict) -> None:
    """Calls the shell script that gathers the tagger dict source files into a single TXT."""
    run_command_with_output(f"bash {TAGGER_BUILD_SCRIPT_PATH}", env=env)


def build_pos_binary() -> None:
    cmd_build = (
        f"java -cp {LT_JAR_PATH} "
        f"org.languagetool.tools.POSDictionaryBuilder "
        f"-i {RESULT_POS_DICT_FILEPATH} "
        f"-info {POS_INFO_JAVA_INPUT_PATH} "
        f"-o {POS_DICT_JAVA_OUTPUT_PATH}"
    )
    run_command(cmd_build)
    shutil.copy(POS_INFO_JAVA_INPUT_PATH, POS_INFO_JAVA_OUTPUT_PATH)


def build_synth_binary() -> None:
    cmd_build = (
        f"java -cp {LT_JAR_PATH} "
        f"org.languagetool.tools.SynthDictionaryBuilder "
        f"-i {RESULT_POS_DICT_FILEPATH} "
        f"-info {SYNTH_INFO_JAVA_INPUT_PATH} "
        f"-o {SYNTH_DICT_JAVA_OUTPUT_PATH}"
    )
    run_command_with_output(cmd_build, env={**os.environ})
    shutil.copy(SYNTH_INFO_JAVA_INPUT_PATH, SYNTH_INFO_JAVA_OUTPUT_PATH)
    shutil.move(path.join(JAVA_OUTPUT_DIR, "portuguese_synth.dict_tags.txt"),
                path.join(JAVA_OUTPUT_DIR, "portuguese_tags.txt"))


def main():
    SHELL_ENV = set_shell_env()
    compile_lt_dev()
    run_shell_script(SHELL_ENV)
    build_pos_binary()
    build_synth_binary()


if __name__ == "__main__":
    main()
