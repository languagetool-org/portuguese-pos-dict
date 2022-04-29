use strict;
use warnings;
use autodie;
use utf8;

binmode( STDOUT, ":utf8" );

my @files = ( "adjectives-fdic.txt", "nouns-fdic.txt", "verbs-fdic.txt");
my %lemmas;
my $file;

foreach $file (@files) {
	open(my $fh,  "<:encoding(UTF-8)", "../src-dict/".$file);
		while (my $line = <$fh>) {
	    chomp($line);
	    if ($line =~ /^([^# =]+)/) {       
	        my $lemma=$1;
	        $lemmas{$lemma}=1;
	    }
	}
	close ($fh);
}

@files = ( "adverbs-lt.txt", "adv_mente-lt.txt", "propernouns-lt.txt", "resta-lt.txt");
foreach $file (@files) {
	open(my $fh,  "<:encoding(UTF-8)", "../src-dict/".$file);
		while (my $line = <$fh>) {
	    chomp($line);
	    if ($line =~ /^.* (.*) .*$/) {       
	        my $lemma=$1;
	        $lemmas{$lemma}=1;
	    }
	}
	close ($fh);
}

open(my $ofh,  ">:encoding(UTF-8)", "br-pt_excluding.txt");
open(my $ofh2,  ">:encoding(UTF-8)", "br-pt_recommend-BR.txt");
open(my $ofh3,  ">:encoding(UTF-8)", "br-pt_uncertain.txt");

foreach my $lemma (sort keys %lemmas) {
	if ($lemma =~ /ê/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/ê/é/;
		if (exists($lemmas{$lemma2})) {
			print $ofh "$lemma=$lemma2\n";
		}
	}
	if ($lemma =~ /ô/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/ô/ó/;
		if (exists($lemmas{$lemma2})) {
			print $ofh "$lemma=$lemma2\n";
		}
	}

	if ($lemma =~ /pt/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/pt/t/;
		if (exists($lemmas{$lemma2})) {
			print $ofh2 "$lemma2=$lemma\n";
		}
	}
	if ($lemma =~ /cç/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/cç/ç/;
		if (exists($lemmas{$lemma2})) {
			print $ofh2 "$lemma2=$lemma\n";
		}
	}

	if ($lemma =~ /ct/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/ct/t/;
		if (exists($lemmas{$lemma2})) {
			print $ofh3 "$lemma2=$lemma\n";
		}
	}
	# recepção
	if ($lemma =~ /pç/) {
		my $lemma2 = $lemma;
		$lemma2 =~ s/pç/ç/;
		if (exists($lemmas{$lemma2})) {
			print $ofh3 "$lemma=$lemma2\n";
		}
	}
}

close($ofh);