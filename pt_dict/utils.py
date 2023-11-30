import shlex
import subprocess
from os import chdir, path
from typing import List

import random

from pt_dict.constants import LOGGER, LT_DIR, REPO_DIR, RESULTS_DIR
from pt_dict.dicts.dictionary import Dictionary
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.dicts.tagger import TaggerDict

SOURCE_LEXICON_MAPPING = {
    'hunspell': HunspellDict,
    'tagger': TaggerDict
}


def get_source_dict(name: str) -> Dictionary:
    return SOURCE_LEXICON_MAPPING.get(name)()


def compile_lt_dev():
    """Build with maven in the languagetool-dev directory."""
    LOGGER.info("Compiling LT dev...")
    chdir(path.join(LT_DIR, "languagetool-dev"))
    run_command("mvn clean compile assembly:single")
    chdir(REPO_DIR)  # Go back to the repo directory


def install_dictionaries():
    """Install our dictionaries, I hope."""
    LOGGER.info("Installing dictionaries...")
    chdir(RESULTS_DIR)
    run_command("mvn clean install")
    chdir(REPO_DIR)  # Go back to the repo directory


def run_command(command: str) -> bytes:
    """Execute the given shell command and return its output."""
    LOGGER.debug(f"Running command: {command}")
    result = subprocess.run(shlex.split(command), capture_output=True)
    if result.returncode != 0:
        msg = f"Command failed with error code {result.returncode}: {result.stderr}"
        LOGGER.warn(msg)
        raise RuntimeError(msg)
    return result.stdout


def run_command_with_input(command: str, input_data: str) -> str:
    """Execute a shell command with the provided input and return its output."""
    LOGGER.debug(f"Running command with piped stdin: {command}")
    process = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout_data, stderr_data = process.communicate(input=input_data)  # Feeding input data and collecting output
    if process.returncode != 0:
        msg = f"Command failed with error code {process.returncode}: {stderr_data}"
        LOGGER.warn(msg)
        raise RuntimeError(msg)
    return stdout_data


def print_sample(word_list: List[str], sample_size: int):
    print(', '.join(sorted(word_list, key=lambda i: random.random())[0:sample_size]))
