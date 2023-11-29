#!/bin/bash
lt_per_a_comparar="results/lt/dict.txt"
dir_programes="test-lt-fdic-lt"
dir_intermedi="test-lt-fdic-lt/intermedi"
dir_resultat="results/test-lt-fdic-lt"

rm -rf $dir_intermedi
mkdir $dir_intermedi
echo "Splitting and sorting LT dict"
perl $dir_programes/separa-reordena-lt.pl $lt_per_a_comparar $dir_intermedi
for i in $dir_intermedi/sorted-*.txt
do
    export LC_ALL=C && sort $i -o $i
done

echo "Adjectives: LT to FDIC"
perl lt-to-fdic/lt-to-fdic.pl adjectives $dir_intermedi
echo "Nouns: LT to FDIC"
perl lt-to-fdic/lt-to-fdic.pl nouns $dir_intermedi
echo "Verbs: LT to FDIC"
mkdir $dir_intermedi/models-verbals
rm $dir_intermedi/models-verbals/*
perl lt-to-fdic/extrau-verbs-i-models.pl lt-to-fdic $dir_intermedi

#exit

echo "Nouns: FDIC to LT..."
perl fdic-to-lt/flexiona.pl $dir_intermedi/nouns-fdic.txt $dir_intermedi/nouns-lt.txt
echo "Adjectives: FDIC to LT..."
perl fdic-to-lt/flexiona.pl $dir_intermedi/adjectives-fdic.txt $dir_intermedi/adjectives-lt.txt
echo "Verbs: FDIC to LT..."
perl fdic-to-lt/conjuga-verbs.pl $dir_intermedi/verbs-fdic.txt $dir_intermedi/verbs-lt.txt $dir_intermedi/models-verbals/

echo "Checking diffs"

echo "*** DIFFS ***" > $dir_resultat/diff.txt
for i in nouns adjectives verbs
do
    echo "** Compare $i **" >> $dir_resultat/diff.txt
    export LC_ALL=C && sort $dir_intermedi/$i.txt -o $dir_intermedi/$i.txt
    export LC_ALL=C && sort $dir_intermedi/$i-lt.txt -o $dir_intermedi/$i-lt.txt
    diff $dir_intermedi/$i.txt $dir_intermedi/$i-lt.txt >> $dir_resultat/diff.txt
done
echo "** Other errors **" >> $dir_resultat/diff.txt
grep "#" $lt_per_a_comparar >> $dir_resultat/diff.txt
grep "ERROR" $lt_per_a_comparar >> $dir_resultat/diff.txt

#rm -rf $dir_intermedi

echo "Done! Results at $dir_resultat"
