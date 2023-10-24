"""This was translated from shell to python iteratively and interactively using ChatGPT 4."""
import logging
import subprocess
import shlex
from sys import stdout
from typing import List
import chardet as chardet
import concurrent.futures
from tempfile import NamedTemporaryFile
from os import path, chdir, replace

from pt_dict.constants import DICT_DIR, HUNSPELL_DIR, LT_DIR, REPO_DIR, LT_JAR_PATH
from pt_dict.variants.variant import Variant, VARIANTS

TMP_DIR = path.join(DICT_DIR, "tmp")

# negative for no sample ;)
SAMPLE_SIZE = -1

# 20k should split the pt_BR hunspell dic into 16 parts
CHUNK_SIZE = 20000

LOGGER = logging.Logger(name='build_spelling_dicts')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler(stdout))

FORCE_COMPILE = False


def split_dic_file(dic_path, chunk_size):
    """
    Splits a dictionary file into smaller files (chunks) of a given number of lines.

    :param dic_path: Path to the dictionary file.
    :param chunk_size: Number of lines per chunk.
    :return: List of paths to the chunks.
    """
    try:
        with open(dic_path, 'r', encoding='utf-8') as dic_file:
            lines = dic_file.readlines()
    except UnicodeDecodeError:
        with open(dic_path, 'r', encoding='ISO-8859-1') as dic_file:
            lines = dic_file.readlines()
    if SAMPLE_SIZE > 0:
        lines = lines[0:SAMPLE_SIZE]
    total_lines = len(lines)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    chunk_paths = []
    for index, chunk in enumerate(chunks):
        chunk_path = dic_path.replace('.dic', f'_chunk{index}.dic').replace(HUNSPELL_DIR, TMP_DIR)
        try:
            with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                chunk_file.writelines(chunk)
        except UnicodeEncodeError:
            with open(chunk_path, 'w', encoding='ISO-8859-1') as chunk_file:
                chunk_file.writelines(chunk)
        chunk_paths.append(chunk_path)
    return chunk_paths


def compile_lt_dev():
    """Build with maven in the languagetool-dev directory."""
    LOGGER.info("Compiling LT dev...")
    chdir(path.join(LT_DIR, "languagetool-dev"))
    run_command("mvn clean compile assembly:single")
    chdir(REPO_DIR)  # Go back to the repo directory


def run_command(command: str) -> str:
    """Execute the given shell command and return its output."""
    LOGGER.info(f"Running command: {command}")
    result = subprocess.run(shlex.split(command), capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed with error code {result.returncode}: {result.stderr}")

    output: bytes = result.stdout
    encoding_detected = chardet.detect(output)["encoding"]
    if encoding_detected == "ISO-8859-1":
        return output.decode('ISO-8859-1')
    return output.decode('utf-8')


def run_command_with_input(command: str, input_data: str) -> str:
    """Execute a shell command with the provided input and return its output."""
    LOGGER.info(f"Running command with piped stdin: {command}")
    process = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout_data, stderr_data = process.communicate(input=input_data)  # Feeding input data and collecting output
    if process.returncode != 0:
        raise RuntimeError(f"Command failed with error code {process.returncode}: {stderr_data}")
    return stdout_data


def unmunch(variant: Variant, chunk_path: str) -> tuple[NamedTemporaryFile, str]:
    """Create all forms from Hunspell dictionaries."""
    unmunched_tmp = NamedTemporaryFile(delete=False)
    LOGGER.info(f"Unmunching {path.basename(chunk_path)} into {unmunched_tmp.name}...")
    cmd_unmunch = f"unmunch {chunk_path} {variant.aff()}"
    result_unmunch = run_command(cmd_unmunch)
    with open(unmunched_tmp.name, "w") as f:
        f.write(result_unmunch)
    return unmunched_tmp, variant.hyphenated


def build_binary(unmunched_tmps: List[NamedTemporaryFile], variant: Variant):
    LOGGER.info(f"Building binary for {variant}...")
    megatemp = NamedTemporaryFile(delete=True)
    lines = []
    for tmp in unmunched_tmps:
        with open(tmp.name, 'r') as t:
            lines.extend(t.read().split("\n"))
    with open(megatemp.name, 'w') as f:
        f.write("\n".join(sorted(set(lines))))
    cmd_build = (
        f"java -cp {LT_JAR_PATH} "
        f"org.languagetool.tools.SpellDictionaryBuilder "
        f"-i {megatemp.name} "
        f"-info {variant.info('source')} "
        f"-freq {variant.freq()} "
        f"-o {variant.dict()}"
    )
    run_command(cmd_build)
    LOGGER.info(f"Done compiling {variant} dictionary!")
    replace(variant.info('source'), variant.info('target'))
    megatemp.close()


def main():
    if FORCE_COMPILE:
        compile_lt_dev()
    tasks = []
    unmunched_files = {}
    for variant in VARIANTS:
        unmunched_files[variant.hyphenated] = []
        chunk_paths = split_dic_file(variant.dic(), CHUNK_SIZE)
        for chunk_path in chunk_paths:
            tasks.append((variant, chunk_path))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        tmp_files = executor.map(lambda task: unmunch(task[0], task[1]), tasks)
        for file, var_code in tmp_files:
            unmunched_files[var_code].append(file)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda var: build_binary(unmunched_files[var.hyphenated], var), VARIANTS)


if __name__ == "__main__":
    main()
