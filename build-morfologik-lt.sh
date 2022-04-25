#!/bin/bash

cd morfologik-lt


#LanguageTool jar
#jarfile=~/github/languagetool/languagetool-tools/target/languagetool-tools-3.5-SNAPSHOT-jar-with-dependencies.jar
jarfile=~/target-lt/languagetool.jar

target_dir=../results/java-lt/src/main/resources/org/languagetool/resource/pt

#source dictionaries
# spanish
cp ../results/lt/dict.txt /tmp/portuguese.txt

for targetdict in portuguese
do
    
    # replace whitespaces with tabs
    perl sptotabs.pl </tmp/${targetdict}.txt >${targetdict}_tabs.txt

    # create tagger dictionary with morfologik tools
    # -freq es_wordlist.xml
    java -cp $jarfile org.languagetool.tools.POSDictionaryBuilder -i ${targetdict}_tabs.txt -info ${targetdict}.info -o ${targetdict}.dict

    # dump the tagger dictionary
    java -cp $jarfile org.languagetool.tools.DictionaryExporter -i ${targetdict}.dict -info ${targetdict}.info -o ${targetdict}_lt.txt

    # create synthesis dictionary with morfologik tools
    java -cp $jarfile org.languagetool.tools.SynthDictionaryBuilder -i ${targetdict}_tabs.txt -info ${targetdict}_synth.info -o ${targetdict}_synth.dict
    
    mv ${targetdict}_synth.dict_tags.txt ${targetdict}_tags.txt

    # dump synthesis dictionary
    java -cp $jarfile org.languagetool.tools.DictionaryExporter -i ${targetdict}_synth.dict -o ${targetdict}_synth_lt.txt -info ${targetdict}_synth.info

    rm ${targetdict}_tabs.txt

    #convert catalan_tags.txt to DOS file
    sed 's/$'"/`echo \\\r`/" ${targetdict}_tags.txt > ${targetdict}_tags_dos.txt
    rm ${targetdict}_tags.txt
    mv ${targetdict}_tags_dos.txt ${targetdict}_tags.txt

    cp ${targetdict}_tags.txt $target_dir
    cp ${targetdict}.dict $target_dir
    cp ${targetdict}_synth.dict $target_dir
    cp ${targetdict}.info $target_dir
    cp ${targetdict}_synth.info $target_dir
done