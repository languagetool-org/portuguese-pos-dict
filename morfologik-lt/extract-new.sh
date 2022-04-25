#!/bin/bash

###
# Extrau les novetats introduïdes en el diccionari LT
# respecte a l'última versió compilada
###

#directori LanguageTool
#lt_tools=~/github/languagetool/languagetool-tools/target/languagetool-tools-3.5-SNAPSHOT-jar-with-dependencies.jar
#lt_tools=~/languagetool/languagetool.jar
lt_tools=~/target-lt/languagetool.jar

# dump the tagger dictionary
java -cp $lt_tools org.languagetool.tools.DictionaryExporter -i es-ES.dict -o es-ES_lt.txt -info es-ES.info

cp es-ES_lt.txt diccionari_antic.txt
echo "Preparant diccionari"
sed -i 's/^\(.*\)\t\(.*\)\t\(.*\)$/\1 \2 \3/' diccionari_antic.txt
echo "Ordenant diccionari"
export LC_ALL=C && sort -u diccionari_antic.txt -o diccionari_antic.txt
echo "Comparant diccionaris"
diff ../results/lt/diccionari.txt diccionari_antic.txt > diff.txt

echo "Extraient novetats"
grep -E "^< " diff.txt > added-body.txt
sed -i 's/^< //g' added-body.txt
sed -i 's/ /\t/g' added-body.txt
cp added-body.txt novetats_sense_tag.txt
sed -i 's/^\(.*\)\t\(.*\)\t\(.*\)$/\1/' novetats_sense_tag.txt
sed -i '/^\s*$/d' novetats_sense_tag.txt
export LC_ALL=C && sort -u novetats_sense_tag.txt -o novetats_sense_tag.txt
cat spelling.head novetats_sense_tag.txt > spelling.txt
cat added-tagger.head added-body.txt > added.txt
cp added.txt /home/jaume/github/languagetool/languagetool-language-modules/es/src/main/resources/org/languagetool/resource/es/
cp spelling.txt /home/jaume/github/languagetool/languagetool-language-modules/es/src/main/resources/org/languagetool/resource/es/hunspell

echo "Extraient paraules esborrades"
grep -E "^> " diff.txt > removed-body.txt
sed -i 's/^> //g' removed-body.txt
sed -i 's/ /\t/g' removed-body.txt
sed -i '/^\s*$/d' removed-body.txt
#cp added-body.txt novetats_sense_tag.txt
#sed -i 's/^\(.*\)\t\(.*\)\t\(.*\)$/\1/' novetats_sense_tag.txt
#sed -i '/^\s*$/d' novetats_sense_tag.txt
#export LC_ALL=C && sort -u novetats_sense_tag.txt -o novetats_sense_tag.txt
#cat spelling.head novetats_sense_tag.txt > spelling.txt
cat removed-tagger.head removed-body.txt > removed.txt
cp removed.txt /home/jaume/github/languagetool/languagetool-language-modules/es/src/main/resources/org/languagetool/resource/es/
#cp spelling.txt /home/jaume/github/languagetool/languagetool-language-modules/es/src/main/resources/org/languagetool/resource/es/hunspell

echo "Results in: spelling.txt added.txt removed.txt"

rm diff.txt
rm added.txt
rm added-body.txt
rm removed-body.txt
rm removed.txt
rm spelling.txt
rm novetats*
