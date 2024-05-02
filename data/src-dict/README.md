# POS Tagger Dictionary

This is the dictionary used by LT's POS tagger.

## Source data

The source data for this dictionary is split into two types of files:
1. **inflected** parts of speech, viz. verbs, nouns and adjectives;
2. **uninflected** parts of speech, i.e. everything else.

### Dialect variation

The source data for the tagger is **not** split along dialect lines. This means Portuguese has
a **single** POS tagger dictionary for **all** varieties, regardless of whether words adhere to
orthographic standards or not.

The primary reason for that is that we want words tagged *even when* they are spelt incorrectly.
Returning a `NULL` tag for words that are known in other varieties might just hamper the
performance of the XML grammar rules.

### Format

⚠️ For **all** files in this directory, make sure you *always* leave one blank line at the end of the file. If you fail
to do this, the scripts that work on these files might merge some lines... There is a script that checks for this that
is run in our build workflow. But still, try to remember to do this.

Source data for inflected words follows a specific pattern.

```bash
$word=$tag;model:$paradigmWord;src: $source;
```
Where
- `$word` is the **lemma** we are tagging;
- `$tag` is the POS label;
- `$paradigmWord` is a special word for which we have defined an inflection paradigm; `$word`
  will be inflected using this model;
- `$source` refers to the source of the entry (not super important).

#### Verb entries

```
ab-rogar=V;model:alugar;src: LT;
ababalhar=V;model:amar;src: LT;
abagaçar=V;model:atiçar;src: LT;
abancar=V;model:colocar;src: LT;
```

#### Noun entries

```
abafarete=M;src: LT;
abafas=FP;src: LT;
abafação [pl. abafações]=F;src: LT;
abafeira=F;src: LT;
abandião [pl. abandiões]=M;src: LT;
abandoador=M;src: LT;
abandonado abandonada=MF;src: LT;
```

Note here that:
- we can define an irregular plural by adding `[pl. $plural_form]` before the `=` sign;
- we can define masculine and feminine equivalents on the same line, tagging them as `MF`;

#### Adjective entries
```
abaixável=A;src: LT;
abajoujado abajoujada [sup. abajoujadíssimo]=A;src: LT;
abaladiço abaladiça=A;src: LT;
```

#### Other entries

The remainder of the categories uses the format `$form $lemma $tags`:

```
alô alô I
ambas ambos DI0FP0
ambas ambos PI0FP000
ambos ambos DI0MP0
ambos ambos PI0MP000
amen amen I
amém amém I
amén amén I
ante ante SPS00
ao a:o SPS00:DA0MS0
aos a:os SPS00:DA0MP0
```

## Scripts

Scripts that work on the POS tagger source files are in [/pos_tagger_scripts](../../pos_tagger_scripts).
See the [README]() in that directory for usage instructions.
