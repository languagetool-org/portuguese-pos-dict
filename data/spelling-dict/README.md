# Portuguese Speller Dictionaries

The files in this directory are [Hunspell](https://github.com/hunspell/hunspell)-format
dictionaries and affix files.

## Varieties

Portuguese has **three** source files used for dictionaries:
- `pt-BR`, with Brazilian orthography compliant with the
  [1990 agreement](https://en.wikipedia.org/wiki/Portuguese_Language_Orthographic_Agreement_of_1990);
- `pt-PT-90`, with European and African orthography compliant with the
  [1990 agreement](https://en.wikipedia.org/wiki/Portuguese_Language_Orthographic_Agreement_of_1990);
- `pt-PT-45`, with European and African orthography compliant with the [1945 agreement](https://en.wikipedia.org/wiki/Reforms_of_Portuguese_orthography)
  but not the [1990](https://en.wikipedia.org/wiki/Portuguese_Language_Orthographic_Agreement_of_1990) one.

The **default** dictionary used for Brazilian Portuguese is the `pt-BR` one. For `pt-PT`, the default
is the `pt-PT-90` variety, whereas African varieties (viz. `pt-AO` and `pt-MZ`) have the pre-1990
orthography set as a default (i.e. `pt-PT-45`).

As of November 2023, there is a plan to allow LT users of `pt-PT`, `pt-AO`, and `pt-MZ` to select
which dictionary they'd like to use as a 'user option', but this is not yet implemented.

## Hunspell files

The main lexicon for each variety is found in the [/hunspell](./hunspell) directory, in the
`.dic` format.

### Encoding
Because of well-known limitations of the `unmunch` command that the Hunspell team have not
addressed (and do not seem very eager to address), all files here **MUST** be in **Latin-1**
(a.k.a. **ISO-8859-1**) encoding.

**Do not re-encode these files**, and beware of this when reading them, opening them, etc.

On *nix systems, you can easily tell what a file's encoding is with the `file` command:
```shell
  file pt_BR.aff
  # must return:
  # pt_BR.aff: ISO-8859 text
```

### Dialect equivalencies

The `pt_PT` dictionaries contain words **all** from `pt_AO` and `pt_MZ` dictionaries.

The `pt_PT*`, `pt_AO`, and `pt_MZ` affix definition files are almost identical. Their prefix
and suffix flags are the same, and so there was no reason to use a separate file for them.

The `pt_BR` file, on the other hand, is completely different. Attempting to unify the logic
between them is futile. For now, it is best that they be kept separate. Which does mean that
`pt_BR` contains more entries than `pt_PT*`.

### Test words

At the top of the file, there are some funny-looking words, like `oogaboogatestword`. These are
used for sanity tests in the Java tests. Do not remove them.

### Affix files

The affix files (`.aff`) are the files responsible for inflecting and deriving dictionary entries.
In standard Hunspell, this is used during lookup. For Morfologik, we will use these files to
`unmunch` the dictionaries, i.e. to expand every possible word and save that into one (very large)
file containing every conceivable word form.

To understand how to use these files, check the
[documentation](https://manpages.ubuntu.com/manpages/trusty/en/man4/hunspell.4.html).

⚠️ 🐛 There are *many* bugs with these affix files. Some forms are not generated, and some incorrect
forms are also output. These files are **fragile** – so be careful when editing them.

### Compound lexicon

In [/hunspell/compounds](./hunspell/compounds), we have three `.dic` files, one for each
variety (viz. `pt_BR`, `pt_PT_90`, and `pt_PT_45`). These files contain **only** compound words
that should be kept hyphenated in the final version of the dictionary.

We use these files because, in the process of generating of binaries, we also **tokenise** the `unmunch`ed list of
word forms. Since the tokenisation depends on the compounds present in the [POS tagging dictionary](../src-dict/README.md),
we would end up splitting many hyphenated compounds that exist in the Hunspell source data but not in the POS tagger
dictionary source data.

## `.info` files

The info files are used by Morfologik. There is no amazing documentation, but you can check
the [comments in the code itself](https://github.com/morfologik/morfologik-stemming/blob/master/morfologik-speller/src/main/java/morfologik/speller/Speller.java),
it should tell you how to use the different parameters.

The most important options for us are:
- `fsa.dict.speller.equivalent-chars`: this option allows you to set specific pairs of individual
  characters as equivalent (e.g. `c` and `ç`);
- `fsa.dict.speller.replacement-pairs`: this option gives you the option to define longer
  substrings within words to be prioritised, regardless of similarity or frequency (e.g. the
  common error 'vinheram' for 'vieram' can be defined as `vinher vier`).

These lists are hard to maintain and it's easy to mess them up. As of November, there is an idea
to improve the `equivalent-chars` and `replacement-pairs` lists with some kind of automation
that takes data from a more convenient format, but this has not yet been done.

## Frequency lists

Morfologik leverages frequency information to provide users with better suggestions. That is what
the files [pt_BR_wordlist.xml](./pt_BR_wordlist.xml) and [pt_PT_wordlist.xml](./pt_PT_wordlist.xml)
are for.

These files are sourced from [here](https://github.com/mozilla-b2g/gaia/tree/master/apps/keyboard/js/imes/latin/dictionaries).