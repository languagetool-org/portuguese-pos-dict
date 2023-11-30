# portuguese-pos-dict

This repository contains data and tools used to build dictionaries for Portuguese.

## Maintainer

The owner, maintainer, and main dev for this repository is @p-goulart. The shell and perl components may be better
explained by @jaumeortola, though.

## Dictionaries

Portuguese has **two** separate sets of dictionaries, with separate source data and scripts to handle them:

- **[speller dictionaries](data/spelling-dict/README.md)**: those used by the `MORFOLOGIK_RULE_PT_*` spelling rules for
  all Portuguese varieties;
- **[POS tagger dictionary](data/src-dict/README.md)**: those used by LT's part-of-speech tagger to add POS information
  to each word.

For more in-depth information about each type, check their respective READMEs.

## Scripts

This repository contains two independent sets of scripts:
- for work with the **POS tagger dictionary**, use the bash and Perl scripts in [/pos_tagger_scripts](./pos_tagger_scripts/README.md);
- to build the **speller dictionary** and several other helper files that go in the LT repo, configure Poetry for this
  project and use the Python scripts in [/pt_dict](./pt_dict/README.md).

## Release

TBD
