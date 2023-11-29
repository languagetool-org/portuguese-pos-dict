# POS Tagger Scripts

This directory contains shell and Perl scripts and libraries to be used in the generation of the
Portuguese POS Tagger dictionary.

The source data for these scripts is in [/data/src-dict](../data/src-dict).

## Building

The main script to be explicitly run is `build-lt.sh`, which expands all lemmata from the source
dictionary by generating all inflected forms and outputs a file that can be compiled into the
format used by LT's POS tagger.

To run it, simply call it without any arguments from anywhere:

```shell
./build-lt.sh
```

The output will be saved as a plaintext file called `dict.txt` to the [/results/lt](../results/lt)
directory. This is the only file that is **needed**.

### Requirements

Before running `build-lt.sh`, you must make sure a few things are installed:
- [Perl](https://learn.perl.org/installing/) (`v5.38.0` has been tested on macOS);
- [cpan](https://metacpan.org/dist/CPAN/view/scripts/cpan) or some other program to install Perl
  packages;
- the following Perl packages:
  - `Text::Unaccent::PurePerl`;
  - `Switch`.

This list may not be complete. Please add to it if you find any other dependencies!

## Other scripts

As of November 2023, these scripts are **not** supported, and are therefore found in the `.archive`
subdirectory. Work may be required beforehand if you want to run them (mostly adjusting relative
paths).

- `build-morfogolik-lt.sh` builds a **test** version of a Morfologik-format speller dictionary
  using the source data in [/data/src-dict](../data/src-dict); as of November 2023, this is **not**
  used for anything by LT, and is here only for test/development purposes;
- `extract-new.sh` extracts new entries (when compared to the current state of the dictionary);
- `make-test-lt-fdic.sh` runs a simple test to make sure the dictionary generation is working as
  expected;
- `commit.sh` was a simple script to automate the process of committing changes to the
  dictionary; it deprecated.

## Releasing

To understand the release process, check the corresponding section in the
[main README](../README.md#release).
