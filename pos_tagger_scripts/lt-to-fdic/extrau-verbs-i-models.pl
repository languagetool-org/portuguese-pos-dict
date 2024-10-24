﻿use strict;
use warnings;
use autodie;
use utf8;

binmode(STDOUT, ":utf8");

my $dir_entrada = $ARGV[0];
my $dir_eixida = $ARGV[1];

my $f1 = $dir_eixida."/sorted-verbs.txt";
my $out = $dir_eixida."/models_flexio_verbal.txt";
my $out2 = $dir_eixida."/verbs_no_processats.txt";
my $verbaltagssorted = $dir_entrada."/verbal_tags_sorted.txt";
my $nommodels = $dir_entrada."/nom_models_verbals.txt";
my $verbs_fdic = $dir_eixida."/verbs-fdic.txt";

my $joinpostag=":";
my $inf = "";
my $prevInf = "";
my $model="";
my $word;
my $arrel="";
my $terminacio="";
my $sufix;
my $postag;
my $error=1;
my %models = ();
my %verbs_no_processats = ();
my %model = ();
my $posicions_radical=0;
my $i=0;
my $j=0;
my $l=0;
my @words;
my @postags;
my @sufixos;
my @sufixos_esborrats;


open(my $fh, "<:encoding(UTF-8)", $f1);
open(my $ofh, ">:encoding(UTF-8)", $out);

while(my $line = <$fh>){
    chomp($line);
    if ($line =~ /^([^ ]+) (V.+) ([^ ]+)$/)	{
	$inf=$1;
	$word=$3;
	$postag=$2;

	if ($inf !~ /^$prevInf$/) { #s'acaba el verb

	    if ($model =~ /.+/) {
		if (exists($models{$model})) {
		    $models{$model}.=$prevInf.",";
		}
		else {
		    $models{$model}=",".$prevInf.",";
		}
	    }

	    #comença un verb nou
	    $model=",";
	    $error=0;
	    $i=0;
	    if ($inf =~ /^(.+)(..)$/) {
		$terminacio=$2;
	    }
	}

	#if ($postag !~ /^VMM02S0\+/) { #ignorem de moment les formes amb canvi d'accent: ámalo
	#if ($postag !~ /^.*\+/) { #ignorem de moment les formes amb canvi d'accent: ámalo
	if ($postag !~ /$joinpostag/ || $word =~ /^(érase|dícese)$/) {

		#afegeix forma     encode($enc, $word);
		$words[$i]=$word;
		$postags[$i]=$postag;
		$i++;

		#separa arrel i sufix
		my $found=0;
		my $posicions=1;
		while (!$found) {
		    if ($inf =~ /^(.*)(.{$posicions})$/) {
			$arrel=$1;
			$sufixos_esborrats[$i]=$2;
			if ($word =~ /^$arrel(.*)$/) {
			    $sufixos[$i]=$1;
			    if ($sufixos[$i] =~ /^$/) {
				$sufixos[$i]="0";
			    }
			    $found=1;
			}
		    }
		    $posicions++;
		}

		if ($found) {
		    $model.=$sufixos_esborrats[$i]." ".$sufixos[$i]." ".$terminacio." ".$postag.",";
		}
		else {
		    print "error en: $inf $word $postag";
		}

	}

	

	$prevInf=$inf;
	#print $ofh "$prevInf $inf $arrel $model $error\n";
    }
}
# Afegeix l'últim verb
if ($model =~ /.+/) {
    if (exists($models{$model})) {
	$models{$model}.=$prevInf.",";
    }
    else  {
	$models{$model}=",".$prevInf.",";
    }
}
close($fh);


# Llegeix l'ordre dels postags
open(my $fh2, '<:encoding(UTF-8)', $verbaltagssorted)
    or die "Could not open file!";
chomp(my @postags_sorted = <$fh2>);

# Llegeix la numeració dels models
open(my $fh3, '<:encoding(UTF-8)', $nommodels )
    or die "Could not open file!";
my %modelnumber=();
my $count=1;
while (<$fh3>) {
    chomp($_);
    if (/^(.+)$/) {
	$modelnumber{$1}=$count;
	$count++;
	#print "$1 $modelnumber{$1}\n";
    }
}

# Obre arxiu de format de diccionari
open(my $ofhfdic, ">:encoding(UTF-8)", $verbs_fdic);

my $key;
my $value;
my $myPostag;
my $k;
my $v;
my $notrobats ="";
while (($key, $value) = each %models) {
    my $modelnum=0;
    my $modelverb="0";
    #print "$value\n";
    my $verbs_model=$value;
    #print "$verbs_model\n";
    keys %modelnumber;
    while (($k,$v) = each %modelnumber) {
	$value=$verbs_model;
	#print $ofh "$k\n";
	if ($value =~ /,$k,/) {
	    $modelnum=$v;
	    $modelverb=$k;
	    $modelnumber{$k}=0;
	    last;
	}
    }
    if ($modelverb =~ /^0$/) {
    	$notrobats .= "\n".$verbs_model;
		#Error no correspon a cap model
		next;
    }

    print $ofh "#\n# MODEL: $modelnum $modelverb\n";
    print $ofh "$key\n";
    print $ofh "#\n# VERBS: $verbs_model\n#\n";

    my @verbsdelmodel = split(/,/, $verbs_model);
    foreach my $entradaverb (@verbsdelmodel) {
		if ($entradaverb =~ /.+/) {
		    print $ofhfdic "$entradaverb=V;model:$modelverb;fonts: LT;\n";
		}
    }

    print $ofh "#\n# NO TROBATS: $notrobats\n#\n";

    # Escriu tots els models verbals en arxius separats. Ex: cantar.model.
    open(my $ofhmodel, ">:encoding(UTF-8)", $dir_eixida."/models-verbals/".$modelverb.".model");
    my $myMatch;
    foreach $myPostag (@postags_sorted) {
	my @matches = ($key =~ /([^ ,]+ [^ ]+ [^ ]+ \Q$myPostag\E),/g);
	for $myMatch (@matches)	{
	    if ($myMatch=~/^([^ ,]+) ([^ ]+) ([^ ]+) (\Q$myPostag\E)$/) {
		my $suf1=$1;
		my $suf2=$2;
		print $ofhmodel "$suf1 $suf2 $3 $4";
		my $exemple= $modelverb;
		if ($suf2 =~ /^0$/) { $suf2="";}
		$exemple =~ s/$suf1$/$suf2/;
		print $ofhmodel " # $exemple\n";
	    }
	}
    }
    close ($ofhmodel);
}
close ($ofhfdic);


print $ofh "Models no usats\n";
while (($k,$v) = each %modelnumber) {
    print $ofh "$k $v\n" if ($v>0);
}

close($ofh);


