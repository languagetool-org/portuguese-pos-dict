"""This was translated from shell to python iteratively and interactively using ChatGPT 4."""
import shutil
from datetime import datetime
from typing import List
import concurrent.futures
from tempfile import NamedTemporaryFile
from os import path

from pt_dict.constants import DICT_DIR, HUNSPELL_DIR, LT_JAR_PATH, LOGGER
from pt_dict.utils import run_command, compile_lt_dev
from pt_dict.variants.variant import Variant, DIC_VARIANTS

TMP_DIR = path.join(DICT_DIR, "tmp")

# negative for no sample ;)
SAMPLE_SIZE = -1

# 20k should split the pt_BR hunspell dic into 16 parts
CHUNK_SIZE = 20000
MAX_THREADS = 8

FORCE_COMPILE = False


def split_dic_file(dic_path: str, chunk_size: int) -> List[str]:
    """Splits a dictionary file into smaller files (chunks) of a given number of lines."""
    with open(dic_path, 'r', encoding='ISO-8859-1') as dic_file:
        lines = dic_file.readlines()[1:]  # Skip the first line
    lines = [line for line in lines if not line.startswith("#")]  # Filter out comment lines
    if SAMPLE_SIZE > 0:
        lines = lines[0:SAMPLE_SIZE]
    total_lines = len(lines)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    chunk_paths = []
    for index, chunk in enumerate(chunks):
        chunk_path = dic_path.replace('.dic', f'_chunk{index}.dic').replace(HUNSPELL_DIR, TMP_DIR)
        with open(chunk_path, 'w', encoding='ISO-8859-1') as chunk_file:
            chunk_file.writelines(chunk)
        chunk_paths.append(chunk_path)
    return chunk_paths


def unmunch(variant: Variant, chunk_path: str) -> tuple[NamedTemporaryFile, str]:
    """Create all forms from Hunspell dictionaries.

    Args:
        variant: a Variant object, the source of the dictionary data
        chunk_path: a path to a dic file chunk

    Returns:
        a tuple containing the tmp file and the code of the COUNTRY association of the variant; this is because
        some variants (viz. AO and MZ) supply entries for the PT dictionary, not their own variety.
    """
    unmunched_tmp = NamedTemporaryFile(delete=False, mode='wb')
    LOGGER.debug(f"Unmunching {path.basename(chunk_path)} into {unmunched_tmp.name}...")
    cmd_unmunch = f"unmunch {chunk_path} {variant.aff()}"
    result_unmunch = run_command(cmd_unmunch)
    unmunched_tmp.write(result_unmunch)
    unmunched_tmp.flush()
    unmunched_tmp.close()
    return unmunched_tmp, variant.association


def build_binary(unmunched_tmps: List[NamedTemporaryFile], variant: Variant):
    LOGGER.info(f"Building binary for {variant}...")
    megatemp = NamedTemporaryFile(delete=True, mode='w', encoding='utf-8')  # Open the file with UTF-8 encoding
    lines = set()
    for tmp in unmunched_tmps:
        with open(tmp.name, 'r', encoding='ISO-8859-1') as t:  # Open the file with ISO-8859-1 encoding
            lines.update(t.read().split("\n"))
    # Since megatemp is opened in 'w' mode with UTF-8 encoding, it will write in UTF-8 directly
    megatemp.write("\n".join(sorted(lines)))
    LOGGER.debug(f"Found {len(lines)} unique unmunched forms for {variant}.")
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
    if FORCE_COMPILE:
        compile_lt_dev()
    tasks = []
    unmunched_files = {}
    # TODO: at some point we need to manage the pre and post-agreement distinction here
    # the whole 'dict_variant' will need to go, and we will just merge all the unmunched files into one big one
    # and then split them based on the dialectal and pre/post agreement alternation files
    for variant in DIC_VARIANTS:
        unmunched_files[variant.association] = []
        chunk_paths = split_dic_file(variant.dic(), CHUNK_SIZE)
        for chunk_path in chunk_paths:
            tasks.append((variant, chunk_path))
    LOGGER.info("Starting unmunching process...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        tmp_files = executor.map(lambda task: unmunch(task[0], task[1]), tasks)
        for file, variant_association_code in tmp_files:
            unmunched_files[variant_association_code].append(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(lambda var: build_binary(unmunched_files[var.association], var), DIC_VARIANTS)
    LOGGER.debug(f"finished at {datetime.now().strftime('%r')}")


if __name__ == "__main__":
    main()
