#!/bin/perl
use strict;
use warnings;
use autodie;
use utf8;
use FindBin;
use lib "$FindBin::Bin/../libs";
use Flexio;

binmode( STDOUT, ":utf8" );

my $input_path   = $ARGV[0];
my $output_path  = $ARGV[1];
my $models_dir   = $ARGV[2];

open( my $input_file,  "<:encoding(UTF-8)", $input_path );
open( my $output_file, ">:encoding(UTF-8)", $output_path );

while (my $line = <$input_file>) {
    chomp($line);
    if ($line =~ /^([^#].+)=(.+?);model:(.+?);/) {
        my $infinitive = $1;
        my $category = $2;
        my $model = $3;
        open( my $model_file,  "<:encoding(UTF-8)", $models_dir.$model.".model" );
        while (my $model_line = <$model_file>) {
            if ($model_line !~ /^#/ && $model_line =~ /^(.+) (.+) (.+) (.+) #.*$/) {
                my $form = $infinitive;
                my $to_remove = $1;
                my $to_add = $2;
                my $postag = $4;
                if ($form =~ /^(.*)$to_remove$/) {
                    $form = $1;
                } else {
                    warn "ERROR in $output_file";
                }
                if ($to_add !~ /^0$/) {
                    $form .= $to_add;
                }
                print $output_file "$form	$infinitive	$postag\n";
                print $output_file Flexio::verb_pronouns($form, $infinitive, $postag);
            }
        }
    close ($model_file);
    }
}
close ($output_file);
close ($input_file);
