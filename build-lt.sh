#!/bin/bash

cd src-dict
./sort-all.sh
cd ..

dir_resultat="results/lt"
rm $dir_resultat/*.txt
echo "Noms: de FDIC a LT..."
perl fdic-to-lt/flexiona.pl src-dict/noms-fdic.txt $dir_resultat/noms-lt.txt
echo "Adjectius: de FDIC a LT..."
perl fdic-to-lt/flexiona.pl src-dict/adjectius-fdic.txt $dir_resultat/adjectius-lt.txt
echo "Verbs: de FDIC a LT..."
perl fdic-to-lt/conjuga-verbs.pl src-dict/verbs-fdic.txt $dir_resultat/verbs-lt.txt src-dict/models-verbals/
echo "Afegint la resta de categories..."
cat src-dict/*-lt.txt > $dir_resultat/others-lt.txt

#remove comments
echo "Removing comments..."
sed -i 's/ *#.*$//' $dir_resultat/others-lt.txt
sed -i -E 's/\s+$//' $dir_resultat/others-lt.txt
sed -i '/^$/d' $dir_resultat/others-lt.txt

cat $dir_resultat/*-lt.txt > $dir_resultat/diccionari.txt
rm $dir_resultat/*-lt.txt

# sort
export LC_ALL=C && sort -u $dir_resultat/diccionari.txt > $dir_resultat/diccionari_sorted.txt
rm $dir_resultat/diccionari.txt
mv $dir_resultat/diccionari_sorted.txt $dir_resultat/diccionari.txt

diff $dir_resultat/diccionari.old $dir_resultat/diccionari.txt > $dir_resultat/diccionari.diff
echo "Resultat en el directori $dir_resultat/diccionari.diff"
echo "FET!"

grep "ERROR" results/lt/diccionari.txt

git --no-pager diff --no-index $dir_resultat/diccionari.old $dir_resultat/diccionari.txt

