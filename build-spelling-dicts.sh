#!/bin/sh

# `unmunch` is a command from the Hunspell library: https://github.com/hunspell/hunspell
# `languagetool-dev-6.3-SNAPSHOT-jar-with-dependencies.jar` is built with 'mvn clean compile assembly:single' in languagetool-dev
# `languagetool.jar` is built with 'mvn clean package -DskipTests' in languagetool

ltDir="../languagetool"
ltVer="6.3-SNAPSHOT"

#variants="BR PT AO MZ"
variants="BR"
lang="pt"

rm -rf spelling-dict/tmp
mkdir spelling-dict/tmp

for variant in $variants
do
	echo ${lang}_${variant}
	# create all forms from Hunspell dictionaries
	unmunch spelling-dict/hunspell/${lang}_${variant}.dic spelling-dict/hunspell/${lang}_${variant}.aff | sort -u > spelling-dict/tmp/${lang}_${variant}1.txt
	# convert to UTF-8
	if [ "$variant" = "BR" ]
	then
		cat spelling-dict/tmp/${lang}_${variant}1.txt | iconv -f ISO-8859-1 -t UTF-8 > spelling-dict/tmp/${lang}_${variant}2.txt
		mv spelling-dict/tmp/${lang}_${variant}2.txt spelling-dict/tmp/${lang}_${variant}1.txt
	fi
	# tokenize all forms with LT tokenizer
	cat spelling-dict/tmp/${lang}_${variant}1.txt | java -cp ${ltDir}/languagetool-standalone/target/LanguageTool-${ltVer}/LanguageTool-${ltVer}/languagetool.jar:$ltDir/languagetool-dev/target/languagetool-dev-${ltVer}-jar-with-dependencies.jar org.languagetool.dev.archive.WordTokenizer $lang | sort -u > spelling-dict/tmp/${lang}_${variant}2.txt
	# differences after tokenization
	diff spelling-dict/tmp/${lang}_${variant}1.txt spelling-dict/tmp/${lang}_${variant}2.txt > spelling-dict/tmp/${lang}_${variant}.diff
done
