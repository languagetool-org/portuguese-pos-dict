#!/bin/sh

# `unmunch` is a command from the Hunspell library: https://github.com/hunspell/hunspell
# `languagetool-dev-6.3-SNAPSHOT-jar-with-dependencies.jar` is built with 'mvn clean compile assembly:single' in languagetool-dev
# `languagetool.jar` is built with 'mvn clean package -DskipTests' in languagetool

ltDir="../languagetool"
ltVer="6.3-SNAPSHOT"

#cd ${ltDir}
#mvn clean package -DskipTests
#cd -
cd ${ltDir}/languagetool-dev
mvn clean compile assembly:single
cd -

variants="BR PT AO MZ"
#variants="BR"
lang="pt"

#rm -rf spelling-dict/tmp
mkdir spelling-dict/tmp

for variant in $variants
do
	echo "Unmunching ${lang}_${variant}..."
	# create all forms from Hunspell dictionaries
	unmunch spelling-dict/hunspell/${lang}_${variant}.dic spelling-dict/hunspell/${lang}_${variant}.aff | sort -u > spelling-dict/tmp/${lang}_${variant}1.txt
	# convert to UTF-8
	if [ "$variant" = "BR" ]
	then
		cat spelling-dict/tmp/${lang}_${variant}1.txt | iconv -f ISO-8859-1 -t UTF-8 > spelling-dict/tmp/${lang}_${variant}2.txt
		mv spelling-dict/tmp/${lang}_${variant}2.txt spelling-dict/tmp/${lang}_${variant}1.txt
	fi
	# tokenize all forms with LT tokenizer
	echo "Tokenizing ${lang}_${variant}..."
	cat spelling-dict/tmp/${lang}_${variant}1.txt | java -cp ${ltDir}/languagetool-standalone/target/LanguageTool-${ltVer}/LanguageTool-${ltVer}/languagetool.jar:$ltDir/languagetool-dev/target/languagetool-dev-${ltVer}-jar-with-dependencies.jar org.languagetool.dev.archive.WordTokenizer $lang | sort -u > spelling-dict/tmp/${lang}_${variant}2.txt
	# differences after tokenization
	#diff spelling-dict/tmp/${lang}_${variant}1.txt spelling-dict/tmp/${lang}_${variant}2.txt > spelling-dict/tmp/${lang}_${variant}.diff

	#TODO: merge spelling.txt, prohibit.txt, added.txt, removed.txt... ?

	# build binary
	freqDict="pt_PT_wordlist.xml"
	if [ "$variant" = "BR" ]
	then
		freqDict=pt_BR_wordlist.xml
	fi
	outputDir="results/java-lt/src/main/resources/org/languagetool/resource/pt/hunspell"
	java -cp ${ltDir}/languagetool-standalone/target/LanguageTool-${ltVer}/LanguageTool-${ltVer}/languagetool.jar org.languagetool.tools.SpellDictionaryBuilder -i spelling-dict/tmp/${lang}_${variant}2.txt -info spelling-dict/${lang}_${variant}.info -freq spelling-dict/${freqDict} -o ${outputDir}/${lang}-${variant}.dict
	cp spelling-dict/${lang}-${variant}.info ${outputDir}
done
