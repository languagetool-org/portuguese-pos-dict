use strict;
use warnings;
use autodie;
use utf8;
use Switch;
require "./libs/Flexio.pm";

binmode( STDOUT, ":utf8" );

#my $arxiucategoria = $ARGV[0];  # adjectius, noms

my $f1  = $ARGV[0];    # "../lt-to-fdic/".$arxiucategoria."-fdic.txt";
my $out = $ARGV[1];    # $arxiucategoria."-lt.txt";

my $out2 = "mots_no_processats.txt";

my $mot_masc;
my $mot_fem;
my $numAccepcio;
my $tagbefore;
my $tagafter;
my $excepcions;

open( my $fh,  "<:encoding(UTF-8)", $f1 );
open( my $ofh, ">:encoding(UTF-8)", $out );

while ( my $line = <$fh> ) {
    chomp($line);
    my $categoria;
    my $found = 0;


    #Superlatiu: abrandat abrandada [sup. abrandadíssim]
    if ( $line =~ /^($Flexio::carac+) .*\[sup\. ([^ ]+)o\]/ ) {
        my $lemma = $1;
        my $superlatiu = $2;
        my $tag = "AQ";
        if ($line =~ /categories: AO/) {
          $tag="AO";
          }
        print $ofh "${superlatiu}o ${superlatiu}o ${tag}AMS0\n";
        print $ofh $superlatiu."a ${superlatiu}o ${tag}AFS0\n";
        print $ofh $superlatiu."os ${superlatiu}o ${tag}AMP0\n";
        print $ofh $superlatiu."as ${superlatiu}o ${tag}AFP0\n";
        #print $ofh "$superlatiu $lemma AQAMS0\n";
        #print $ofh $superlatiu."a $lemma AQAFS0\n";
        #print $ofh $superlatiu."s $lemma AQAMP0\n";
        #print $ofh $superlatiu."es $lemma AQAFP0\n";
    }

    if ( $line =~ /^($Flexio::carac+) .*\[sup\. ([^ ]+)o o ([^ ]+)o\]/ ) {
        my $lemma = $1;
        my $superlatiu = $2;
        my $superlatiu2 = $3;
        print $ofh "${superlatiu}o ${superlatiu}o AQAMS0\n";
        print $ofh $superlatiu."a ${superlatiu}o AQAFS0\n";
        print $ofh $superlatiu."os ${superlatiu}o AQAMP0\n";
        print $ofh $superlatiu."as ${superlatiu}o AQAFP0\n";

        print $ofh "${superlatiu2}o ${superlatiu2}o AQAMS0\n";
        print $ofh $superlatiu2."a ${superlatiu2}o AQAFS0\n";
        print $ofh $superlatiu2."os ${superlatiu2}o AQAMP0\n";
        print $ofh $superlatiu2."as ${superlatiu2}o AQAFP0\n";

        #print $ofh "$superlatiu $lemma AQAMS0\n";
        #print $ofh $superlatiu."a $lemma AQAFS0\n";
        #print $ofh $superlatiu."s $lemma AQAMP0\n";
        #print $ofh $superlatiu."es $lemma AQAFP0\n";
    }

    #
    # A partir de dues formes, masculí i femení. Ex.: valencià -ana.
    #

    if ($line =~ /^($Flexio::carac+) ($Flexio::carac+)(.*)=categories: ([AMF].*?);/ )
    {
        $mot_masc   = $1;
        $excepcions = $3;
        $categoria  = $4;

        ( $mot_fem, $found ) =
          Flexio::desplega_femeni_amb_guionet( $mot_masc, $2 );

        if ( !$found ) {
            print $ofh "***POSSIBLE ERROR*** $line\n";
            next;
        }

        $numAccepcio = "";
        #if ( $mot_masc !~ /$Flexio::number_exceptions/ )
        #{    # Excepció: el número forma part del mot
        #    if ( $mot_masc =~ /^(.+)([0-9])$/ ) {
        #        $mot_masc    = $1;
        #        $numAccepcio = $2;
        #    }
        #}

        my $fp  = "";
        my $mp  = "";
        my $ms2 = "";
        my $mp2 = "";
        my $fs2 = "";
        my $mp3 = "";
        my $fs3 = "";

        $mp = Flexio::plural( $mot_masc, "M" );
        if ( $excepcions =~ /\[pl\. ([^ ]+?)\]/ ) {
            $mp = $1;
        }
        elsif ( $excepcions =~ /\[pl\. (.+?) o (.+?) o (.+?)\]/ ) {
            $mp  = $1;
            $mp2 = $2;
            $mp3 = $3;
        }
        elsif ( $excepcions =~ /\[pl\. (.+?) o (.+?)\]/ ) {
            $mp  = $1;
            $mp2 = $2;
        }
=pod
        # plural a partir del femení
        elsif (
            $mot_masc =~ /.+([àéèíóòú]|[aàeéèiíoóòuú][sn]|ix)$/ )
        {
            $mp = Flexio::pluralMasc_del_fem($mot_fem);
        }
        else {
            # dobles formes de plural
            if ( $mp =~ /^(.+s)([tc])s$/ ) {
                $mp2 = $1 . $2 . "os";
            }
            elsif ( $mp =~ /^(.+xt)s$/ ) {
                $mp2 = $1 . "os";
            }

            # roigs rojos
            elsif ( $mp =~ /^(.+[aeou])igs$/ ) {
                $mp2 = $1 . "jos";
            }
        }
=cut
        if ( $excepcions =~ /\[fem\. ([^ ]+?) o ([^ ]+?)\]/ ) {    #forma extra de femení
            $fs2 = $1;
            $fs3 = $2;
        }
        elsif ( $excepcions =~ /\[fem\. ([^ ]+?)\]/ ) {    #forma extra de femení
            $fs2 = $1;
        }
        if ( $excepcions =~ /\[masc\. ([^ ]+?)\]/ ) { #forma extra de masculí (bon)
            $ms2 = $1;
        }

        $fp = Flexio::plural( $mot_fem, "F" );

        #accentuació valenciana
        if ( $mot_masc =~ /^(.+)è([sn]?)$/ ) {
            $ms2 = $1 . "é" . $2;
        }

        #print "$mot_masc $mot_fem $mp $mp2 $fp\n";

        #Imprimir formes etiquetades
        $tagbefore = "";
        $tagafter  = "";
        switch ($categoria) {
            case "MF" { $tagbefore = "NC";  $tagafter = "000"; }
            case "A"  { $tagbefore = "AQ0"; $tagafter = "0"; }
            case "AA" { $tagbefore = "AQA"; $tagafter = "0"; }
            case "AO" { $tagbefore = "AO0"; $tagafter = "0"; }
        }

        print $ofh "$mot_masc $mot_masc$numAccepcio $tagbefore" . "MS"
          . "$tagafter\n";
        if ( $ms2 =~ /.+/ ) {
            print $ofh "$ms2 $mot_masc$numAccepcio $tagbefore" . "MS"
              . "$tagafter\n";
        }
        print $ofh "$mot_fem $mot_masc$numAccepcio $tagbefore" . "FS"
          . "$tagafter\n";
        if ( $mp2 =~ /.+/ ) {
            print $ofh "$mp2 $mot_masc$numAccepcio $tagbefore" . "MP"
              . "$tagafter\n";
        }
        if ( $mp3 =~ /.+/ ) {
            print $ofh "$mp3 $mot_masc$numAccepcio $tagbefore" . "MP"
              . "$tagafter\n";
        }
        if ( $mp !~ /^$fp$/ ) {
            print $ofh "$mp $mot_masc$numAccepcio $tagbefore" . "MP"
              . "$tagafter\n";
            print $ofh "$fp $mot_masc$numAccepcio $tagbefore" . "FP"
              . "$tagafter\n";
        }
        else {
            print $ofh "$mp $mot_masc$numAccepcio $tagbefore" . "CP"
              . "$tagafter\n";
        }

        # forma femenina extra
        if ( $fs2 =~ /.+/ ) {
            print $ofh "$fs2 $mot_masc$numAccepcio $tagbefore" . "FS"
              . "$tagafter\n";
            my $fp2 = Flexio::plural( $fs2, "F" );
            print $ofh "$fp2 $mot_masc$numAccepcio $tagbefore" . "FP"
              . "$tagafter\n";
        }
        if ( $fs3 =~ /.+/ ) {
            print $ofh "$fs3 $mot_masc$numAccepcio $tagbefore" . "FS"
              . "$tagafter\n";
            my $fp3 = Flexio::plural( $fs3, "F" );
            print $ofh "$fp3 $mot_masc$numAccepcio $tagbefore" . "FP"
              . "$tagafter\n";
        }

        # ?????
        if ( $mot_masc =~ /^$mp$/ || $mot_fem =~ /^$fp$/ ) {
            print $ofh "***POSSIBLE ERROR*** $line\n";
        }
    }

    #
    # Una única forma. Ex.: taula.
    #

    elsif ( $line =~ /^([^#].*)=categories: ([AMF].*?);/ ) {

        $categoria = $2;
        my $entrada         = $1;
        my $singular        = "";
        my $plural          = "";
        my $plural2         = "";
        my $plural3         = "";
        my $singular2       = "";
        my $femeniplural    = "";
        my $femenisingular2 = "";
        $numAccepcio = "";

        #forma bàsica primera
        if ( $entrada =~ /^($Flexio::carac+)/ ) {
            $singular    = $1;
            $numAccepcio = "";
            #if ( $singular !~ /$Flexio::number_exceptions/ )
            #{    # Excepció: el número forma part del mot
            #    if ( $singular =~ /^(.+)([0-9])$/ ) {
            #        $singular    = $1;
            #        $numAccepcio = $2;
            #    }
            #}
        }
        if ( $categoria =~ /F/ && $categoria !~ /M/ ) {
            $plural = Flexio::plural( $singular, "F", "F" )
              ;    #les larinxs, falçs, calçs
        }
        else {
            $plural = Flexio::plural( $singular, "M" );
        }
        if ( $categoria =~ /I$/ )    #Invarible
        {
            $plural = $singular;
        }
        elsif ( $entrada =~ /\[pl\. (.+?) o (.+?) o (.+?)\]/ )
        {    # dues excepcions de plural
            $plural       = $1;
            $femeniplural = $1;
            $plural2      = $2;
            $plural3      = $3;
        }
        elsif ( $entrada =~ /\[pl\. ([^ ]+?)\]/ ) {    #una excepció de plural
            $plural       = $1;
            $femeniplural = $1;
        }
        elsif ( $entrada =~ /\[pl\. (.+?) o (.+?)\]/ )
        {    # dues excepcions de plural
            $plural       = $1;
            $femeniplural = $1;
            $plural2      = $2;
        }

        if ( $entrada =~ /\[fem\. (.+)]/ ) {    # una forma extra femení
            $femenisingular2 = $1;
        }

        $tagbefore = "";
        $tagafter  = "";
        if ( $categoria =~ /^[MF]/ ) {
            $tagbefore = "NC";
            $tagafter  = "000";
        }
        elsif ( $categoria =~ /^AO/ ) {
            $tagbefore = "AO0";
            $tagafter  = "0";
        }
        elsif ( $categoria =~ /^AA/ ) {
            $tagbefore = "AQA";
            $tagafter  = "0";
        }
        elsif ( $categoria =~ /^A/ ) {
            $tagbefore = "AQ0";
            $tagafter  = "0";
        }

        #noms
        if ( $categoria =~ /I$/ ) {
            if ( $categoria =~ /MF/ ) {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "CN"
                  . "$tagafter\n";
                if ( $singular2 =~ /.+/ ) {
                    print $ofh "$singular2 $singular$numAccepcio $tagbefore"
                      . "CN"
                      . "$tagafter\n";
                }
            }
            elsif ( $categoria =~ /F/ ) {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "FN"
                  . "$tagafter\n";
                if ( $singular2 =~ /.+/ ) {
                    print $ofh "$singular2 $singular$numAccepcio $tagbefore"
                      . "FN"
                      . "$tagafter\n";
                }
            }
            elsif ( $categoria =~ /M/ ) {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "MN"
                  . "$tagafter\n";
                if ( $singular2 =~ /.+/ ) {
                    print $ofh "$singular2 $singular$numAccepcio $tagbefore"
                      . "MN"
                      . "$tagafter\n";
                }
            }
            else {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "CN"
                  . "$tagafter\n";
                if ( $singular2 =~ /.+/ ) {
                    print $ofh "$singular2 $singular$numAccepcio $tagbefore"
                      . "CN"
                      . "$tagafter\n";
                }
            }
        }
        elsif ( $categoria =~ /^(MF|A|AA|AO)$/ ) {
            if ( $singular =~ $plural ) {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "CN"
                  . "$tagafter\n";
            }
            else {
                print $ofh "$singular $singular$numAccepcio $tagbefore" . "CS"
                  . "$tagafter\n";
                if ( $singular2 =~ /.+/ ) {
                    print $ofh "$singular2 $singular$numAccepcio $tagbefore"
                      . "CS"
                      . "$tagafter\n";
                }
                if ( $femeniplural =~ /^$/ ) {
                    $femeniplural = Flexio::plural( $singular, "F" );
                }
                if ( $plural =~ /$femeniplural/ ) {
                    print $ofh "$plural $singular$numAccepcio $tagbefore" . "CP"
                      . "$tagafter\n";
                    if ( $plural2 =~ /.+/ ) {
                        print $ofh "$plural2 $singular$numAccepcio $tagbefore"
                          . "CP"
                          . "$tagafter\n";
                    }
                }
                else {
                    print $ofh "$plural $singular$numAccepcio $tagbefore" . "MP"
                      . "$tagafter\n";
                    print $ofh "$femeniplural $singular$numAccepcio $tagbefore"
                      . "FP"
                      . "$tagafter\n";    #sequaces
                }

                # forma femenina extra
                if ( $femenisingular2 =~ /.+/ ) {
                    print $ofh
                      "$femenisingular2 $singular$numAccepcio $tagbefore" . "FS"
                      . "$tagafter\n";
                    my $femeniplural2 = Flexio::plural( $femenisingular2, "F" );
                    print $ofh "$femeniplural2 $singular$numAccepcio $tagbefore"
                      . "FP"
                      . "$tagafter\n";
                }
            }
        }
        elsif ( $categoria =~ /MFS/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "CS"
              . "$tagafter\n";
            if ( $singular2 =~ /.+/ ) {
                print $ofh "$singular2 $singular$numAccepcio $tagbefore" . "CS"
                  . "$tagafter\n";
            }
        }
        elsif ( $categoria =~ /MS/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "MS"
              . "$tagafter\n";
            if ( $singular2 =~ /.+/ ) {
                print $ofh "$singular2 $singular$numAccepcio $tagbefore" . "MS"
                  . "$tagafter\n";
            }
        }
        elsif ( $categoria =~ /MP/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "MP"
              . "$tagafter\n";
            if ( $plural2 =~ /.+/ ) {
                print $ofh "$plural2 $singular$numAccepcio $tagbefore" . "MP"
                  . "$tagafter\n";    ## ???
            }
            if ( $plural3 =~ /.+/ ) {
                print $ofh "$plural3 $singular$numAccepcio $tagbefore" . "MP"
                  . "$tagafter\n";    ## ???
            }
        }
        elsif ( $categoria =~ /FS/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "FS"
              . "$tagafter\n";
        }
        elsif ( $categoria =~ /FP/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "FP"
              . "$tagafter\n";
        }
        elsif ( $categoria =~ /MI/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "MN"
              . "$tagafter\n";
            if ( $singular2 =~ /.+/ ) {
                print $ofh "$singular2 $singular$numAccepcio $tagbefore" . "MN"
                  . "$tagafter\n";
            }
        }
        elsif ( $categoria =~ /M/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "MS"
              . "$tagafter\n";
            print $ofh "$plural $singular$numAccepcio $tagbefore" . "MP"
              . "$tagafter\n";
            if ( $plural2 =~ /.+/ ) {
                print $ofh "$plural2 $singular$numAccepcio $tagbefore" . "MP"
                  . "$tagafter\n";
            }
            if ( $plural3 =~ /.+/ ) {
                print $ofh "$plural3 $singular$numAccepcio $tagbefore" . "MP"
                  . "$tagafter\n";
            }
            if ( $singular2 =~ /.+/ ) {
                print $ofh "$singular2 $singular$numAccepcio $tagbefore" . "MS"
                  . "$tagafter\n";
            }
        }
        elsif ( $categoria =~ /FI/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "FN"
              . "$tagafter\n";
        }
        elsif ( $categoria =~ /F/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "FS"
              . "$tagafter\n";
            if ( $singular2 =~ /.+/ ) {
                print $ofh "$singular2 $singular$numAccepcio $tagbefore" . "FS"
                  . "$tagafter\n";
            }

#		if ($femeniplural !~ /.+/) {
#		    $femeniplural = Flexio::plural($singular, "F"); #Atenció: forests (no forestos)
#		}
            print $ofh "$plural $singular$numAccepcio $tagbefore" . "FP"
              . "$tagafter\n";
            if ( $plural2 =~ /.+/ ) {
                print $ofh "$plural2 $singular$numAccepcio $tagbefore" . "FP"
                  . "$tagafter\n";
            }
            elsif ( $singular2 =~ /.+/ ) {
                my $femeniplural2 = Flexio::plural( $singular2, "F", "F" );
                print $ofh "$singular2 $femeniplural2$numAccepcio $tagbefore"
                  . "FP"
                  . "$tagafter\n";    #???
            }
        }
        elsif ( $categoria =~ /S/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "CS"
              . "$tagafter\n";
        }
        elsif ( $categoria =~ /P/ ) {
            print $ofh "$singular $singular$numAccepcio $tagbefore" . "CP"
              . "$tagafter\n";
        }

    }
    elsif ($line =~ /^($Flexio::carac+)=categories: (RG);/ )
    {
        print $ofh "$1 $1 RG\n";
    }
    else {
        #print "$line\n";
    }

}
close($fh);
close($ofh);
