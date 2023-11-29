#!/bin/sh

# `unmunch` is a command from the Hunspell library: https://github.com/hunspell/hunspell
# `languagetool-dev-6.4-SNAPSHOT-jar-with-dependencies.jar` is built with 'mvn clean compile assembly:single' in languagetool-dev
# `languagetool.jar` is built with 'mvn clean package -DskipTests' in languagetool

if [[ -z $LT_HOME ]]; then
  ltDir="../languagetool"
else
  ltDir="${LT_HOME}"
fi

ltVer="6.4-SNAPSHOT"

lang="pt"
variants="BR PT AO MZ"
outputDir="results/java-lt/src/main/resources/org/languagetool/resource/pt/spelling"

#cd ${ltDir}
#mvn clean package -DskipTests
#cd -
cd ${ltDir}/languagetool-dev
mvn clean compile assembly:single
cd -

#rm -rf spelling-dict/tmp
mkdir -p spelling-dict/tmp

for variant in $variants; do
	echo "Unmunching ${lang}_${variant}..."
	# create all forms from Hunspell dictionaries
	unmunch data/spelling-dict/hunspell/${lang}_${variant}.dic spelling-dict/hunspell/${lang}_${variant}.aff 2>>unmunch.log | sort -u > data/spelling-dict/tmp/${lang}_${variant}1.txt
	# convert to UTF-8
	if [[ "$variant" == "BR" ]]; then
		cat data/spelling-dict/tmp/${lang}_${variant}1.txt | iconv -f ISO-8859-1 -t UTF-8 > spelling-dict/tmp/${lang}_${variant}2.txt
		mv data/spelling-dict/tmp/${lang}_${variant}2.txt data/spelling-dict/tmp/${lang}_${variant}1.txt
	fi
	# tokenize all forms with LT tokenizer
	echo "Tokenizing ${lang}_${variant}..."
	cat data/spelling-dict/tmp/${lang}_${variant}1.txt | java -cp ${ltDir}/languagetool-standalone/target/LanguageTool-${ltVer}/LanguageTool-${ltVer}/languagetool.jar:$ltDir/languagetool-dev/target/languagetool-dev-${ltVer}-jar-with-dependencies.jar org.languagetool.dev.archive.WordTokenizer $lang | sort -u > data/spelling-dict/tmp/${lang}_${variant}2.txt
	# differences after tokenization
	#diff spelling-dict/tmp/${lang}_${variant}1.txt spelling-dict/tmp/${lang}_${variant}2.txt > spelling-dict/tmp/${lang}_${variant}.diff

	#TODO: merge spelling.txt, prohibit.txt, added.txt, removed.txt... ?

	# build binary
  freqDict="pt_PT_wordlist.xml"
	if [[ "$variant" == "BR" ]]; then
		freqDict=pt_BR_wordlist.xml
	fi
	java -cp ${ltDir}/languagetool-standalone/target/LanguageTool-${ltVer}/LanguageTool-${ltVer}/languagetool.jar org.languagetool.tools.SpellDictionaryBuilder -i data/spelling-dict/tmp/${lang}_${variant}2.txt -info data/spelling-dict/${lang}-${variant}.info -freq data/spelling-dict/${freqDict} -o ${outputDir}/${lang}-${variant}.dict
	cp data/spelling-dict/${lang}-${variant}.info ${outputDir}
done
