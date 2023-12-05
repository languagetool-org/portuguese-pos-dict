# Dictionary Data

This directory contains the source data for the [POS tagger dictionary](./src-dict/README.md) and the
[Hunspell-format source data](./spelling-dict/README.md) for the speller dictionary, as well as various other files.
For more information about the first two, check their respective READMEs. This README is here only to describe the
**other** files.

## Alternations

The files in the [/alternations](./alternations) directory gather, well, *alternations* between forms of words. Some
spellings are only accepted in Brazilian or European dictionaries, and some spellings are only admissible when using
a specific orthographic standard (e.g. pre/post-1990 agreement).

| filename                                                    | content                                                               | usage                                                                                                                           |
|-------------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| [arbitrary.txt](./alternations/arbitrary.txt)               | PT/BR arbitrary orthographic alternations (no specific pattern)       | concatenated with the other PT/BR alternations files, sorted, uniqued, and piped to `pt_br.txt`                                 |
| [final-stress.txt](./alternations/final-stress.txt)         | PT/BR alternations in the openness of stressed, word-final mid vowels | concatenated with the other PT/BR alternations files, sorted, uniqued, and piped to `pt_br.txt`                                 |
| [pre-nasal-accent.txt](./alternations/pre-nasal-accent.txt) | PT/BR alternations in the openness of stressed, pre-nasal mid vowels  | concatenated with the other PT/BR alternations files, sorted, uniqued, and piped to `pt_br.txt`                                 |
| [silent-letters.txt](./alternations/silent-letters.txt)     | PT/BR alternations in the presence/absence of silent consonants       | concatenated with the other PT/BR alternations files, sorted, uniqued, and piped to `pt_br.txt`                                 |
| [pt_45_90.tsv](./alternations/pt_45_90.tsv)                 | European Portuguese alternations pre- and post-1990 agreement         | used by the [split_variants](../pt_dict/scripts/split_variants.py) script                                                       |
| [pt_br.txt](./alternations/pt_br.txt)                       | the final, uniqued list out of all the PT/BR files here               | copied to `resource/pt/dialect_alternations.txt`, and used by the [split_variants](../pt_dict/scripts/split_variants.py) script |

Out of these, only [pt_br.txt](./alternations/pt_br.txt) sees the light of day: it gets copied to the LT repo, as the
`resource/pt/dialect_alternations.txt` file. It is then used by the Morfologik Java rule to provide users with more
specific messages (and, potentially, at some point also the possibility to switch to the other variety).

## Ignore

The files in [./ignore](./ignore) are used to generate the contents of the `ignore.txt` file that the LT rule uses. The
words contained here are weird but *mostly* correct. We don't want to flag them, but we also do not want to provide them
to users as suggestions.

## Prohibit

Much like the [ignore](#ignore) files above, these are words to be moved to the `prohibit.txt` file, and used by LT.
They contain words that should **not** be allowed, even if they are present in the Hunspell source data. Ideally, this
file will be empty, as we can just adjust the source data not to contain illegal words, but this may not always be very
straightforward due to unforeseen effects of [affixation](./spelling-dict/README.md#affix-files).

## Miscellaneous

The files in [misc](./misc) are, well, a bit of a hodgepodge.

### Names

The [names.txt](./misc/names.txt) file is a collection of given names and surnames taken from various sources. They are
kept separate because, depending on the performance, we may want to have them in either in the main dictionary or in
the ignore file.

### Abbreviations

The [abbreviations.txt](./misc/abbreviations.txt) file contains a list of entries extracted from the `pt_BR.dic`
Hunspell dictionary representing a number of standard abbreviations. Because of how word tokenisation is done, it was
necessary to add some specific logic to the Portuguese Morfologik Java rule to accept these abbreviations, **but only**
when they are followed by a full stop. This file is added **directly** to `resource/pt/abbreviations.txt` in the LT
repo.

### Offensive words

The [offensive.dic](./misc/offensive.dic) file contains a list of profanity, insults, racial slurs, words of sexual
content and otherwise 'controversial' words. While we want to recognise these words and not flag them as spelling
mistakes, we do **not** want to suggest them to users.

The word list contained in this file is tagged using the suffixes from the
[Brazilian Portuguese affix file](./spelling-dict/hunspell/pt_BR.aff). As such, the generation of the final word list is
done with a simple `unmunch` statement like so:

```bash
unmunch ./misc/offensive.dic ./spelling-dict/hunspell/pt_BR.aff > ./misc/offensive.out
```

Note that the source file, like all Hunspell source files, **must** be kept in Latin-1 encoding, and likewise the output
will always be encoded that way. The output file must be copied to `resource/pt/do_not_suggest.txt`, where it will be
used by the speller Java rule, but it must first be converted to UTF-8. Something like this should work:

```bash
iconv -t UTF-8 -f ISO-8859-1 ./misc/offensive.out > ./misc/offensive_utf8.out
```

### Syllables

The [syllables.tsv](./misc/syllables.tsv) file is a tab-separated file containing syllabification data for *all* words
found in the Hunspell *and* POS Tagger dictionaries at some point. It is only here to bootstrap the process of finding
pre-nasal alternation pairs. It is used by the [syllabify](../pt_dict/scripts/syllabify.py) script.

## Words to be added

The files in the [to_add](./to_add) directory are... well, just a collection of words from the older version of the
`spelling.txt` file from the LT repo. They were generated mostly manually, and were processed using the
[clean_migration_files](../pt_dict/scripts/clean_migration_files.py) script.

This is mostly kept here for historical purposes... don't do anything with these files without talking to the LT PT team
first.

