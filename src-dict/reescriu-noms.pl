use strict;
use warnings;
use autodie;
use utf8;

binmode( STDOUT, ":utf8" );

my %lemes;


open(my $fh,  "<:encoding(UTF-8)", "noms-units-masc-fem-2.txt");
while (my $line = <$fh>) {
    chomp($line);
    if ($line =~ /^([^#].+) (.+)=categories: MF;.+$/) {       
        my $lema=$1;
        my $lema2=$2;
        $lemes{$lema}=1;
        $lemes{$lema2}=1;
    }
}
close ($fh);

open($fh,  "<:encoding(UTF-8)", "noms-fdic.txt");
while (my $line = <$fh>) {
    chomp($line);
    if ($line =~ /^([^#].+)=categories: [MF];.+$/) {       
        my $lema=$1;
        if (not exists $lemes{$lema}) {
            print "$line\n";
        }
    } else {
        print "$line\n";
    }
}
close ($fh);

