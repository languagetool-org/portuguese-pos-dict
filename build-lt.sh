#!/bin/bash

cd src-dict
./sort-all.sh
cd ..

dir_resultat="results/lt"
rm $dir_resultat/*.txt
echo "Nouns: FDIC to LT..."
perl fdic-to-lt/flexiona.pl src-dict/nouns-fdic.txt $dir_resultat/nouns-lt.txt
echo "Adjectives: FDIC to LT..."
perl fdic-to-lt/flexiona.pl src-dict/adjectives-fdic.txt $dir_resultat/adjectives-lt.txt
echo "Verbs: FDIC to LT..."
perl fdic-to-lt/conjuga-verbs.pl src-dict/verbs-fdic.txt $dir_resultat/verbs-lt.txt src-dict/models-verbals/
echo "Remaining categories..."
cat src-dict/*-lt.txt > $dir_resultat/others-lt.txt

#remove comments
echo "Removing comments..."
sed -i 's/ *#.*$//' $dir_resultat/others-lt.txt
sed -i -E 's/\s+$//' $dir_resultat/others-lt.txt
sed -i '/^$/d' $dir_resultat/others-lt.txt

cat $dir_resultat/*-lt.txt > $dir_resultat/dict.txt
rm $dir_resultat/*-lt.txt

# sort
export LC_ALL=C && sort -u $dir_resultat/dict.txt > $dir_resultat/dict_sorted.txt
rm $dir_resultat/dict.txt
mv $dir_resultat/dict_sorted.txt $dir_resultat/dict.txt

diff $dir_resultat/dict.old $dir_resultat/dict.txt > $dir_resultat/dict.diff
echo "Results in folder $dir_resultat/dict.diff"
echo "DONE!"

grep "ERROR" results/lt/dict.txt

git --no-pager diff --no-index $dir_resultat/dict.old $dir_resultat/dict.txt

