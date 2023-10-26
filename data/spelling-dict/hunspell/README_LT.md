# LT use of Hunspell Dictionaries

## Encoding
- because of well-known limitations of the `unmunch` command that the Hunspell team have not addressed (and do not seem
  very eager to address), all files here are in **Latin-1** or **ISO-8859-1** encoding;
- **do not re-encode these files**, and beware of this when reading them, opening them, etc.;
- on *nix systems, you can easily tell what a file's encoding is with the `file` command:
  ```shell
    file pt_BR.aff
    # must return:
    # pt_BR.aff: ISO-8859 text
  ```
  
## Equivalencies
The `pt_PT.dic` file has been merged with the `pt_AO` and `pt_MZ` dictionaries. That is to say: **all** entries in the
lexicons for African Portuguese found in this directory are present in the `pt_PT` file. When using Hunspell, building
dictionary binaries, or `unmunch`ing them for later use by other tools, it should be enough to use `pt_PT`.

The `pt_PT`, `pt_AO`, and `pt_MZ` affix definition files are almost identical. Their prefix and suffix flags are the
same, and there is no reason to use a separate file for them.

The `pt_BR` file, on the other hand, is completely different. Attempting to unify the logic between them is futile.
For now, it is best that they be kept separate.

