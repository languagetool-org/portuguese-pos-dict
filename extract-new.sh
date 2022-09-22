#!/bin/bash

###
# Extract new added and removed words with respect to
# the last compiled version
###

#LanguageTool folder
lt_tools=~/target-lt/languagetool.jar

# dump the tagger dictionary
java -cp $lt_tools org.languagetool.tools.DictionaryExporter -i portuguese.dict -o portuguese_lt.txt -info portuguese.info

cd morfologik-lt

cp portuguese_lt.txt dict_old.txt
echo "Preparing dictionary"
sed -i 's/^\(.*\)\t\(.*\)\t\(.*\)$/\1 \2 \3/' dict_old.txt
echo "Sorting dictionary"
export LC_ALL=C && sort -u dict_old.txt -o dict_old.txt
echo "Comparing dictionaries"
diff ../results/lt/dict.txt dict_old.txt > diff.txt

echo "Extracting new added words"
grep -E "^< " diff.txt > added-body.txt
sed -i 's/^< //g' added-body.txt
sed -i 's/ /\t/g' added-body.txt
cp added-body.txt novetats_sense_tag.txt
sed -i 's/^\(.*\)\t\(.*\)\t\(.*\)$/\1/' novetats_sense_tag.txt
sed -i '/^\s*$/d' novetats_sense_tag.txt
export LC_ALL=C && sort -u novetats_sense_tag.txt -o novetats_sense_tag.txt
cat spelling.head novetats_sense_tag.txt > spelling.txt
cat added-tagger.head added-body.txt > added.txt
echo "# Add entries manually from here" >> added.txt
cp added.txt /home/jaume/github/languagetool/languagetool-language-modules/pt/src/main/resources/org/languagetool/resource/pt/
#cp spelling.txt /home/jaume/github/languagetool/languagetool-language-modules/pt/src/main/resources/org/languagetool/resource/pt/hunspell

echo "Extracting new removed words"
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
echo "# Add entries manually from here" >> removed.txt
cp removed.txt /home/jaume/github/languagetool/languagetool-language-modules/pt/src/main/resources/org/languagetool/resource/pt/
#cp spelling.txt /home/jaume/github/languagetool/languagetool-language-modules/pt/src/main/resources/org/languagetool/resource/pt/hunspell

echo "Results in: spelling.txt added.txt removed.txt"

rm diff.txt
rm added.txt
rm added-body.txt
rm removed-body.txt
rm removed.txt
rm spelling.txt
rm novetats*

cd ..