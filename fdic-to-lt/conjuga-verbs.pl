#!/bin/perl
use strict;
use warnings;
use autodie;
use utf8;
require "./libs/Flexio.pm";

binmode( STDOUT, ":utf8" );

my $f1   = $ARGV[0]; # "../lt-to-fdic/verbs-fdic.txt";
my $out  = $ARGV[1]; #"verbs-lt.txt";
my $modelsdir = $ARGV[2]; #"../lt-to-fdic/models-verbals/";

open( my $fh,  "<:encoding(UTF-8)", $f1 );
open( my $ofh, ">:encoding(UTF-8)", $out );

while (my $line = <$fh>) {
    chomp($line);

    if ($line =~ /^([^#].+)=categories:(.+?);model:(.+?);/) {
        my $infinitiu = $1;
        my $categoria = $2;
        my $model = $3;
        open( my $modelfh,  "<:encoding(UTF-8)", $modelsdir.$model.".model" );
        while (my $modelline = <$modelfh>) {
            if ($modelline !~ /^#/ && $modelline =~ /^(.+) (.+) (.+) (.+) #.*$/) {
                my $forma = $infinitiu;
                my $trau = $1;
                my $afegeix = $2;
                my $postag = $4;
                if ($forma =~ /^(.*)$trau$/) {
                    $forma = $1;
                }
                else {
                    print $ofh "ERROR ";
                }
                if ($afegeix !~ /^0$/) {
                    $forma .= $afegeix;
                }
                #if ($postag !~ /\+/) { # les formes amb pronoms són generades de nou
	                print $ofh "$forma $infinitiu $postag\n";
	                #print $ofh Flexio::verb_pronouns( $forma, $infinitiu, $postag );	
                #}
            }
        }
    close ($modelfh);
    }
}
close ($ofh);
close ($fh);
