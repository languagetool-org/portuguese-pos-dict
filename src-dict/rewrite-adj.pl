use strict;
use warnings;
use autodie;
use utf8;

binmode( STDOUT, ":utf8" );

my %lemmas;


open(my $fh,  "<:encoding(UTF-8)", "issimo.txt");
while (my $line = <$fh>) {
    chomp($line);
    if ($line =~ /^([^#].+) (.+) (.+)$/) {       
        my $form=$1;
        my $lemma=$2;
        $lemmas{$lemma}=$form;
        #print "$lemma $form\n";
    }
}
close ($fh);

open($fh,  "<:encoding(UTF-8)", "adjectives-fdic.txt");
while (my $line = <$fh>) {
    chomp($line);
    if ($line =~ /^(.*) (.*)(=A;.+)$/) {       
        my $lemma=$1;
        my $feminine=$2;
        my $remainder=$3;
        if (exists $lemmas{$lemma}) {
            print "$lemma $feminine [sup. $lemmas{$lemma}]$remainder\n";
        } else {
            print "$line\n";    
        }
    } else {
        print "$line\n";
    }
}
close ($fh);

