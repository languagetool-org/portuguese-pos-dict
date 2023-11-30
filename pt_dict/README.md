# Python utilities for the Portuguese speller

This is a Python module that contains a bunch of scripts used in the process of compiling the Morfologik-format
Portuguese speller dictionaries.

## Setup

### Python dependencies

This is set up as a Poetry project, so you must have [Poetry](https://python-poetry.org/docs/) installed and ready to go.

Make sure you are using a [virtual environment](https://python-poetry.org/docs/managing-environments/) and then:

```bash
poetry install --with test,dev
```

### System dependencies

In addition to the Python dependencies, you will also need to have [Hunspell](https://github.com/hunspell/hunspell)
binaries installed on your system.

The most important one is `unmunch`. Check if it's installed:

```bash
which unmunch
# should return a path to a bin directory, like
# /opt/homebrew/bin/unmunch
```

### LT dependencies

The scripts here also depend on the `languagetool` Java codebase (for word tokenisation).

Make sure you have LT cloned locally, and export the following environment variable in your shell configuration:

```bash
export LT_HOME=/path/to/languagetool
```

If this is not done, the code in this project will set that variable as a default to `../languagetool` (meaning one
directory up from wherever this repo is cloned).

## Usage

### `build_spelling_dicts.py`

As of November 2023, the only script here that we can *safely* say should be run by people, out of the box, is
[build_spelling_dicts](./scripts/build_spelling_dicts.py). This is the main script that takes all the Hunspell and
helper files as input and yields as output binary files to be used by the Morfologik speller.

You can check the usage parameters by invoking it with `--help`:

```bash
poetry run python pt_dict/scripts/build_spelling_dicts.py --help
```

### Everything else

Every other script in the `scripts` directory is **not** safe to use. They require some manual tinkering, pointing
things to _ad hoc_ paths, setting and unsetting constants, etc. Do not run any of them without first talking to the
repository [maintainer](../README.md#maintainer).
