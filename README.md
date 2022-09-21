# portuguese-pos-dict

The data and the scripts in this repositoy help to build a POS tagger dictionay in Portuguese. 

## Source dictionary 

The source data is in the [/src-dict](https://github.com/languagetool-org/portuguese-pos-dict/tree/main/src-dict) folder. Words are in diferent files by category. 

There are two kinds of files: 1. Verbs, nouns and adjectives; 2. The other categories. 

Examples of verb entries:
```
ab-rogar=V;model:alugar;src: LT;
ababalhar=V;model:amar;src: LT;
abagaçar=V;model:atiçar;src: LT;
abancar=V;model:colocar;src: LT;
```

Examples of nouns entries:
```
abafarete=M;src: LT;
abafas=FP;src: LT;
abafação [pl. abafações]=F;src: LT;
abafeira=F;src: LT;
abandião [pl. abandiões]=M;src: LT;
abandoador=M;src: LT;
abandonado abandonada=MF;src: LT;
```

Examples of adjectives entries:
```
abaixável=A;src: LT;
abajoujado abajoujada [sup. abajoujadíssimo]=A;src: LT;
abaladiço abaladiça=A;src: LT;
```

The remainder of categories use the format `form<space>lemma<space>postag`:
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

* `build-lt.sh`: creates all the inflected forms from the source dictionary
