"""This was translated from shell to python iteratively and interactively using ChatGPT 4."""
import argparse
import shutil
from datetime import datetime
from typing import List
import concurrent.futures
from tempfile import NamedTemporaryFile
from os import path

from pt_dict.constants import DICT_DIR, HUNSPELL_DIR, LT_JAR_PATH, LOGGER, LT_DIR, LT_VER, LATIN_1_ENCODING, \
    TWO_WAY_ALTERNATIONS_FILEPATH
from pt_dict.utils import run_command, compile_lt_dev, run_command_with_input, install_dictionaries
from pt_dict.variants.variant import Variant, DIC_VARIANTS


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--tmp-dir', default=path.join(DICT_DIR, "tmp"),
                                 help='Temporary directory for processing. Default is the "tmp" directory inside '
                                      'DICT_DIR.')
        self.parser.add_argument('--delete-tmp', action='store_true', default=False,
                                 help='Delete temporary files after processing. Default is False.')
        self.parser.add_argument('--sample-size', type=int, default=-1,
                                 help='Size of the sample. Use negative for no sample. Default is -1.')
        self.parser.add_argument('--chunk-size', type=int, default=20000,
                                 help='Size of the chunks for splitting. Default is 20000.')
        self.parser.add_argument('--max-threads', type=int, default=8,
                                 help='Maximum number of threads to use. Default is 8.')
        self.parser.add_argument('--force-compile', action='store_true', default=True,
                                 help='Force LT compilation even if not necessary. Default is True.')
        self.args = self.parser.parse_args()


def split_dic_file(dic_path: str, chunk_size: int) -> List[str]:
    """Splits a dictionary file into smaller files (chunks) of a given number of lines."""
    with open(dic_path, 'r', encoding=LATIN_1_ENCODING) as dic_file:
        lines = dic_file.readlines()[1:]  # Skip the first line
    lines = [line for line in lines if not line.startswith("#")]  # Filter out comment lines
    if SAMPLE_SIZE > 0:
        lines = lines[0:SAMPLE_SIZE]
    total_lines = len(lines)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    chunk_paths = []
    for index, chunk in enumerate(chunks):
        chunk_path = dic_path.replace('.dic', f'_chunk{index}.dic').replace(HUNSPELL_DIR, TMP_DIR)
        with open(chunk_path, 'w', encoding=LATIN_1_ENCODING) as chunk_file:
            # Prepend the count of lines in this chunk and then write all lines
            chunk_file.write(f"{len(chunk)}\n")
            chunk_file.writelines(chunk)
        chunk_paths.append(chunk_path)
    return chunk_paths


def unmunch(variant: Variant, chunk_path: str) -> NamedTemporaryFile:
    """Create all forms from Hunspell dictionaries.

    Args:
        variant: a Variant object, the source of the dictionary data
        chunk_path: a path to a dic file chunk

    Returns:
        the temp file containing the unmunched dictionary
    """
    unmunched_tmp = NamedTemporaryFile(delete=DELETE_TMP, mode='wb')
    LOGGER.debug(f"Unmunching {path.basename(chunk_path)} into {unmunched_tmp.name}...")
    cmd_unmunch = f"unmunch {chunk_path} {variant.aff()}"
    unmunch_result = run_command(cmd_unmunch)
    unmunched_tmp.write(unmunch_result)
    unmunched_tmp.flush()
    return unmunched_tmp


def tokenise(variant: Variant, unmunched_file: NamedTemporaryFile) -> NamedTemporaryFile:
    """Tokenise each line of an unmunched file, write it to another temp file and return it.

    The written data looks weird, since the output of the LT word tokeniser inserts newlines between tokens.
    Original line after unmunch:
       "far-se-á"
    Lines after tokenisation:
        "far"
        ""
        "se"
        ""
        "á"
    This may look iffy, but later in the process we will sort and dedupe these files, so don't panic.

    Args:
        variant: the Variant object for which we are building the dictionary; note that, *for now*, tokenisation is
                 a *language* thing, i.e. both pt-BR and pt-PT use `pt` tokenisation rules, there is no difference
                 between variants.
        unmunched_file: the NamedTemporaryFile object for the unmunched file we'll be tokenising

    Returns:
        a NamedTemporaryFile with the result of tokenisation written to it; note this is a UTF-8-encoded file; it is not
        at this stage that we move from latin-1 encoding to UTF-8.
    """
    tokenised_tmp = NamedTemporaryFile(delete=DELETE_TMP, mode='w')
    LOGGER.debug(f"Tokenising {unmunched_file.name} into {tokenised_tmp.name}...")
    tokenise_cmd = (
        f"java -cp {LT_JAR_PATH}:"
        f"{LT_DIR}/languagetool-dev/target/languagetool-dev-{LT_VER}-jar-with-dependencies.jar "
        f"org.languagetool.dev.archive.WordTokenizer {variant.lang}"
    )
    with open(unmunched_file.name, 'r', encoding=LATIN_1_ENCODING) as u:
        unmunched_str = u.read()
    unmunched_file.close()
    tokenisation_result = run_command_with_input(tokenise_cmd, input_data=unmunched_str)
    tokenised_tmp.write(tokenisation_result)
    tokenised_tmp.flush()
    return tokenised_tmp


def process_variant(variant: Variant, chunk_path: str) -> tuple[Variant, NamedTemporaryFile]:
    unmunched_file = unmunch(variant, chunk_path)
    return variant, tokenise(variant, unmunched_file)


def build_binary(tokenised_temps: List[NamedTemporaryFile], variant: Variant):
    LOGGER.info(f"Building binary for {variant}...")
    megatemp = NamedTemporaryFile(delete=DELETE_TMP, mode='w', encoding='utf-8')  # Open the file with UTF-8 encoding
    lines = set()
    for tmp in tokenised_temps:
        with open(tmp.name, 'r', encoding='utf-8') as t:
            lines.update(t.read().split("\n"))
    megatemp.write("\n".join(sorted(lines)))
    LOGGER.debug(f"Found {len(lines)} unique unmunched and tokenised forms for {variant}.")
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
    shutil.copy(variant.info('source'), variant.info('target'))
    megatemp.close()


def main():
    LOGGER.debug(f"started at {datetime.now().strftime('%r')}")
    LOGGER.debug(
        f"Options used:\n"
        f"TMP_DIR: {TMP_DIR}\n"
        f"DELETE_TMP: {DELETE_TMP}\n"
        f"SAMPLE_SIZE: {SAMPLE_SIZE}\n"
        f"CHUNK_SIZE: {CHUNK_SIZE}\n"
        f"MAX_THREADS: {MAX_THREADS}\n"
        f"FORCE_COMPILE: {FORCE_COMPILE}\n"
    )
    if FORCE_COMPILE:
        compile_lt_dev()
    tasks = []
    tokenised_files: dict[str: List[NamedTemporaryFile]] = {}
    # TODO: at some point we need to manage the pre and post-agreement distinction here
    # the whole 'dict_variant' will need to go, and we will just merge all the unmunched files into one big one
    # and then split them based on the dialectal and pre/post agreement alternation files
    for variant in DIC_VARIANTS:
        tokenised_files[variant] = []
        chunk_paths = split_dic_file(variant.dic(), CHUNK_SIZE)
        for chunk_path in chunk_paths:
            tasks.append((variant, chunk_path))
    LOGGER.info("Starting unmunching and tokenisation process...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        tmp_files = executor.map(lambda task: process_variant(task[0], task[1]), tasks)
        for variant, file in tmp_files:
            tokenised_files[variant].append(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(lambda var: build_binary(tokenised_files[var], var), DIC_VARIANTS)
    for file_list in tokenised_files.values():
        for file in file_list:
            file.close()
    install_dictionaries()
    LOGGER.debug(f"finished at {datetime.now().strftime('%r')}")


if __name__ == "__main__":
    cli = CLI()
    args = cli.args
    TMP_DIR = args.tmp_dir
    DELETE_TMP = args.delete_tmp
    SAMPLE_SIZE = args.sample_size
    CHUNK_SIZE = args.chunk_size
    MAX_THREADS = args.max_threads
    FORCE_COMPILE = args.force_compile
    main()
