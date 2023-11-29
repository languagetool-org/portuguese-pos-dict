use strict;
use warnings;
use autodie;
use utf8;

binmode( STDOUT, ":utf8" );

my $f1 = $ARGV[0];
my $dir_output = $ARGV[1]."/";
open( my $fh_input, "<:encoding(UTF-8)", $f1 );

my $nouns = "nouns.txt";
my $adjectives = "adjectives.txt";
my $verbs = "verbs.txt";
my $adv_mente = "adverbs-mente.txt";
my $adverbs = "adverbs.txt";
my $propernouns = "propernouns.txt";
my $remainder = "remainder.txt";

my $o_nouns = "sorted-nouns.txt";
my $o_adjectives = "sorted-adjectives.txt";
my $o_verbs = "sorted-verbs.txt";
my $o_adv_mente = "sorted-adverbs-mente.txt";
my $o_adverbs = "sorted-adverbs.txt";
my $o_propernouns = "sorted-propernouns.txt";
my $o_remainder = "sorted-remainder.txt";

open( my $fh_o_nouns, ">:encoding(UTF-8)", $dir_output.$o_nouns );
open( my $fh_o_adjectives, ">:encoding(UTF-8)", $dir_output.$o_adjectives );
open( my $fh_o_verbs, ">:encoding(UTF-8)", $dir_output.$o_verbs );
open( my $fh_o_adv_mente, ">:encoding(UTF-8)", $dir_output.$o_adv_mente );
open( my $fh_o_propernouns, ">:encoding(UTF-8)", $dir_output.$o_propernouns );
open( my $fh_o_adverbs, ">:encoding(UTF-8)", $dir_output.$o_adverbs );
open( my $fh_o_remainder, ">:encoding(UTF-8)", $dir_output.$o_remainder );

open( my $fh_nouns, ">:encoding(UTF-8)", $dir_output.$nouns );
open( my $fh_adjectives, ">:encoding(UTF-8)", $dir_output.$adjectives );
open( my $fh_verbs, ">:encoding(UTF-8)", $dir_output.$verbs );
open( my $fh_adv_mente, ">:encoding(UTF-8)", $dir_output.$adv_mente );
open( my $fh_propernouns, ">:encoding(UTF-8)", $dir_output.$propernouns );
open( my $fh_adverbs, ">:encoding(UTF-8)", $dir_output.$adverbs );
open( my $fh_remainder, ">:encoding(UTF-8)", $dir_output.$remainder );


while(my $line = <$fh_input>){  
    chomp($line);
    if ($line =~ /^([^ +]+) ([^ +]+) (NC....0)$/)
    { 
	print $fh_nouns "$1 $2 $3\n"; 
	print $fh_o_nouns "$2 $3 $1\n"; 
    }
    elsif ($line =~ /^([^ ]+) ([^ ]+) (A....0)$/)
    { 
	print $fh_adjectives "$1 $2 $3\n";
	print $fh_o_adjectives "$2 $3 $1\n"; 
    }
    elsif ($line =~ /^([^ ]+) ([^ ]+) (V.+)$/)
    { 
	print $fh_verbs "$1 $2 $3\n"; 
	print $fh_o_verbs "$2 $3 $1\n"; 
    }
    elsif ($line =~ /^([^ ]+mente) ([^ ]+) (RG)$/)
    { 
	print $fh_adv_mente "$1 $2 $3\n"; 
	print $fh_o_adv_mente "$2 $3 $1\n"; 
    }
    elsif ($line =~ /^([^ ]+) ([^ ]+) (RG)$/)
    { 
	print $fh_adverbs "$1 $2 $3\n"; 
	print $fh_o_adverbs "$2 $3 $1\n"; 
    }
    elsif ($line =~ /^([^ ]+) ([^ ]+) (NP.+)$/)
    { 
	print $fh_propernouns "$1 $2 $3\n"; 
	print $fh_o_propernouns "$2 $3 $1\n"; 
    } 
    elsif ($line =~ /^([^ ]+) ([^ ]+) (.+)$/)
    {
	print $fh_remainder "$1 $2 $3\n"; 
	print $fh_o_remainder "$2 $3 $1\n"; 
    }
}
close($fh_input); 

close($fh_nouns);
close($fh_adjectives);
close($fh_verbs);
close($fh_adv_mente);
close($fh_propernouns);
close($fh_adverbs);
close($fh_remainder);

close($fh_o_nouns);
close($fh_o_adjectives);
close($fh_o_verbs);
close($fh_o_adv_mente);
close($fh_o_propernouns);
close($fh_o_adverbs);
close($fh_o_remainder);
