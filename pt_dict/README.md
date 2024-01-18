# Python utilities for the Portuguese speller

These are Portuguese-specific, and are used for a number of things, but there are currently very few actual scripts
that you can actually run and that we maintain. Most of the code for actual processing is in the `dict_tools` module.

## Maintainer
@p-goulart

## Setup

### Python dependencies

This is set up as a Poetry project, so you must have [Poetry](https://python-poetry.org/docs/) installed and ready to go.

Make sure you are using a [virtual environment](https://python-poetry.org/docs/managing-environments/) and then:

```bash
poetry install --with test,dev
```
