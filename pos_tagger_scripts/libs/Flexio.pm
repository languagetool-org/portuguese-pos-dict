package Flexio;
use strict;
use warnings;
use utf8;
use Text::Unaccent::PurePerl qw(unac_string);

our $carac="[ôõãÅ₂²³a-zA-ZûêàéèíòóúïüäöîâëÄÖÀÈÉÍÒÓÚÏÜÎÂËçÇñÑáå·0-9'\-:]";
our $number_exceptions="^(?i)(L2|P[345]|MP[34]|A[345]|goma-2|4x4|Covid-19|COVID-19|covid-19|SARS-CoV-2|N95|FFP2|Z80|x64|x86)\$";

my $hacaspirada = "Haarlem|hack.*|Harlem|Haifa|haikus?|haima|haimes|halal|halar|hall.*|Halloweens?|Hamada|Hamas|Hamàs|hamilton.*|Hamlet.*|Hammond|Hampton|handicaps?|Hannover|Hanoi|Hans|Hansa|hardware|harolds?|Harrison|harrods?|harry|Hartmann?|Haruki|Harvard|Harz|Havilland|hawai.*|hawk.*|Haydn|Hayworth|Heard|hearst|Heathrow|heav.*|hegel.*|Heidelberg|Heide[gn].*|Heilig.*|hein.*|Heisen.*|Heitz|Helen|Heming.*|henna|hennes|Henry|Hepburn|herbert.*|Herder|Hereford|Hesse|Hessen|Hewlett.*|Hezboll.+|high.*|hilbert.*|Hilda|hinden.*|hinterlands?|Hitch.*|hitler.*|hobbes.*|hobby|hobbies|Hohen.*|holdings?|hollywood.*|Holmes.*|Holstein|Hong|hongk.+|Honolu.+|Honsh[uū]|h[òo]bbits?|hoover.*|hopkins|Hork.*|horst|H[ou]f.*|Houston|Howard|Hubble|humbold.*|Hume|hunting.*|husseinit.+|Higgs|high|Hill|Himmler|hip-hop|hippies|hippy|Hirado|His|Hubei|Hudson|Hunter|Husserl|Huygens|Utah";

my $jointags = ":";

# Genera el plural a partir del singular.
# En alguns casos cal saber el gènere.
sub plural {
    #my $senseaccents = "[^àèéíòóú]";
    my $paraula=$_[0];
    my $genere_resultat = defined $_[1] ? $_[1] : 'M';
    my $genere_origen = defined $_[2] ? $_[2] : 'M';

    #$paraula=~s/([ãêôaeiouéáóúcktpb])$/$1s/;
    $paraula=~s/([r])$/$1es/;
    
    $paraula=~s/t$/ts/;
    
    $paraula=~s/([áúêíéó].*)il$/$1eis/;
    $paraula=~s/([áúêíéó].*)el$/$1eis/;
    $paraula=~s/([áúêíéó].*)ul$/$1uis/;
    
    
    $paraula=~s/z$/zes/;
    $paraula=~s/ol$/óis/;
    $paraula=~s/el$/éis/;
    $paraula=~s/il$/is/;
    $paraula=~s/ul$/úis/;
    $paraula=~s/ês$/eses/;
    $paraula=~s/és$/eses/;
    
    $paraula=~s/l$/is/;
    $paraula=~s/m$/ns/;
    
    $paraula=~s/([ãêôéóáaeiou])$/$1s/;
    
    
    
    return $paraula;
}

# General el masculí plural a partir del femení

#sub pluralMasc_del_fem {
#    my $paraula=$_[0];
#    $paraula =~ s/xa$/xos/;    
#    $paraula =~ s/sa$/sos/;
#    $paraula =~ s/na$/ns/;
#    $paraula =~ s/a$/es/;
#    return $paraula;
#}

# Genera el singular a partir del plural.
# Només per a alguns casos.
sub singular {
    my $paraula=$_[0];
    $paraula=~s/gües$/gua/;
    $paraula=~s/qües$/qua/;
    $paraula=~s/ques$/ca/;
    $paraula=~s/gues$/ga/;
    $paraula=~s/ces$/ça/;
    $paraula=~s/ges$/ja/;
    $paraula=~s/es$/a/; #ha d'anar el primer
    $paraula=~s/s$//;
    return $paraula;
}

# Genera masculí plural a partir de dues formes
sub mascplural_partintdeduesformes {
    my $ms=$_[0];
    my $fs=$_[1];
    my $mp="";

    if ($ms =~ /^$fs$/) {
       $mp=Flexio::plural($ms); # aborigen
    #}
    #elsif ($ms =~ /.+([àéèíóòú]|[aàeéèiíoóòuú][sn]|ix)$/) {
    #   $mp=Flexio::pluralMasc_del_fem($fs);
    } else {
       $mp=Flexio::plural($ms);
    }
    return $mp;
}

# A partir de "aalenià -ana" torna "aaleniana"

sub desplega_femeni_amb_guionet {
    my $mot_masc = $_[0];
    my $term_fem = $_[1];

    my $arrel = $mot_masc;
    my $mot_fem = $term_fem;  # Si no hi ha guionet, serà la forma definitiva
    my $trobat = 1;
    #my $found;
    
    if ($term_fem =~ /^-/) {
    $term_fem =~ s/-//;
    if ( $term_fem =~ /^a$/ ) {
        $arrel=~s/[eoa]$//;
        $mot_fem=$arrel.$term_fem;
        #$found=1;
    }
    else {
        my $nTerm_fem=&unac_string($term_fem);
        my $nMot_masc=&unac_string($mot_masc);
        $nTerm_fem =~ /^(.).*$/;
        my $firstLetterTerm=$1;
            #La terminació femenina s'ha d'afegir a partir de la vocal tònica.
            #Fem que la forma femenina varie entre 0 i 2 caràcters més que la masculina.
            #És un pegat per a no haver de calcular la síl·laba tònica.
            #A voltes fins i tot és més efectiu (sensoriomotor -motriu, tracofrigi -frígia).
        my $lenTerm1=length($nTerm_fem)-1; if ($lenTerm1<0) {$lenTerm1=0;}
        my $lenTerm2=length($nTerm_fem)-3; if ($lenTerm2<0) {$lenTerm2=0;}
        $nMot_masc =~ /^(.+)$firstLetterTerm.{$lenTerm2,$lenTerm1}$/;
        my $lenArrel=length($1);
        $mot_masc =~ /^(.{$lenArrel}).*$/; #recupera alguna dièresi (caïnià)
        $arrel=$1;
        $mot_fem=$arrel.$term_fem;        
        #$found=1;
            #Si la diferència entre masculí i femení és de més de dos caràcters.
            #Error probable.
        if ( abs(length($mot_fem)-length($mot_masc))>2) {
        $trobat = 0; 
        }
    }
    }
    return ($mot_fem, $trobat);
}

# Retorna 1 si un mot masculí s'ha d'apostrofar
sub apostrofa_masculi {
    my $mot = $_[0];
    if ($mot =~ /^h?[aeiouàèéíòóú]/i && $mot !~ /^(h?[ui][aeioàèéóòu].*|[aeio]|host|$hacaspirada)$/i) {
    return 1;
    }
    if ($mot =~ /^(ió|ions|ionitza.+|h?uix.+|Iowa|Uialfàs|Iu)$/) {
    return 1;
    }
    return 0;
}



# Retorna 1 si un mot femení s'ha d'apostrofar amb "l'"
sub apostrofa_femeni {
    my $mot = $_[0];
    if ($mot =~ /^(h?[aeoàèéíòóú].*|h?[ui][^aeiouàèéíòóúüï]+([aeiou]s?|[ei]n)|urbs|URSS|UJI|11a)$/i 
    && $mot !~ /^(ouija|host|ira|inxa|[aeiou]|efa|hac|ela|ema|en|ena|ene|er|erra|erre|essa|una|$hacaspirada)$/i) {
    return 1;
    }
    return 0;
}

sub verb_pronouns {
    my $form=$_[0];
    my $lemma=$_[1];
    my $postag=$_[2];
    my %pronouns;
    my $result = "";

    my $stem = $form;
    $stem =~ s/ar$/ár/;
    $stem =~ s/er$/ér/;
    $stem =~ s/ir$/ír/;
    $stem =~ s/ando$/ándo/;
    $stem =~ s/endo$/éndo/;
    #$stem =~ s/indo$/índo/;

    #$pronouns{"lo"}="PP3CNA00";
    $pronouns{"lo"}="PP3MSA00";
    $pronouns{"los"}="PP3MPA00";
    $pronouns{"la"}="PP3FSA00";
    $pronouns{"las"}="PP3FPA00";
    $pronouns{"le"}="PP3CSD00";
    $pronouns{"les"}="PP3CPD00";
    
    $pronouns{"me"}="PP1CS000";
    $pronouns{"te"}="PP2CS000";
    $pronouns{"se"}="PP3CN000";
    $pronouns{"nos"}="PP1CP000";
    $pronouns{"os"}="PP2CP000";
   

    if ($postag =~ /V.[NG].*/) {
        foreach my $key ("me", "te", "se", "nos", "os", "lo", "los" , "la", "las" , "le", "les") {
            my $stemhere = $form;
            if ($postag =~ /V.G.*/) {$stemhere = $stem;}
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }
        foreach my $key1 ("me", "te", "se", "nos", "os") {
            foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") {
                $result .= "$stem$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
        #se+
        foreach my $key3 ("me", "te", "nos", "os") {
            $result .= "${stem}se$key3 $lemma $postag$jointags".$pronouns{"se"}."$jointags$pronouns{$key3}\n"
               
        }
        #te+
        foreach my $key3 ("me", "nos") {
            $result .= "${stem}te$key3 $lemma $postag$jointags".$pronouns{"te"}."$jointags$pronouns{$key3}\n"
               
        }                
    } elsif ($postag =~ /V.M.1P./){ 
        $stem =~ s/amos$/ámos/;
        $stem =~ s/emos$/émos/;

        foreach my $key ("me", "te", "nos", "os", "lo", "los" , "la", "las" , "le", "les") { #"se"
            my $stemhere = $stem;
            if ($key =~ /^(nos|os|se)$/) {$stemhere =~ s/s$//;}
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }
        foreach my $key1 ("me", "te", "se", "nos", "os") {
            foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") {
                if ($key1 =~ /^se$/ && $key2 =~ /^les?$/) {next;}
                my $stemhere = $stem;
                if ($key1 =~ /^(nos|os|se)$/) {$stemhere =~ s/s$//;}
                $result .= "$stemhere$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
        #te+
        foreach my $key3 ("me", "nos") {
            $result .= "${stem}te$key3 $lemma $postag$jointags".$pronouns{"te"}."$jointags$pronouns{$key3}\n"
        }  

    } elsif ($postag =~ /V.M.2P./){ 
        $stem =~ s/ad$/ád/;
        $stem =~ s/ed$/éd/;
        $stem =~ s/id$/íd/;

        foreach my $key ("me", "nos", "os", "lo", "los" , "la", "las" , "le", "les") { #"se"    apertium sí: "te",
            my $stemhere = $form;
            if ($key =~ /^(os)$/ && $lemma !~ /^ir$/)  {$stemhere =~ s/d$//; $stemhere =~ s/i$/í/; }  #partíos
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }
        foreach my $key1 ("me",  "se", "nos", "os") {  # apertium sí: "te",
            foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") {
                if ($key1 =~ /^se$/ && $key2 =~ /^les?$/) {next;}
                my $stemhere = $stem;
                if ($key1 =~ /^os$/ && $lemma !~ /^ir$/) {$stemhere =~ s/d$//;}
                $result .= "$stemhere$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
        foreach my $key1 ("os") {  
            foreach my $key2 ("me", "nos") {
                my $stemhere = $stem;
                if ($key1 =~ /^(os)$/ && $lemma !~ /^ir$/) {$stemhere =~ s/d$//;}
                $result .= "$stemhere$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
        #te+
        foreach my $key3 ("me", "nos") {
            $result .= "${stem}te$key3 $lemma $postag$jointags".$pronouns{"te"}."$jointags$pronouns{$key3}\n"  
        }  

    } elsif ($postag =~ /V.M.2V./){ 
        $stem =~ s/a$/á/;
        $stem =~ s/e$/é/;
        $stem =~ s/i$/í/;

        foreach my $key ("me", "nos", "os", "lo", "los" , "la", "las" , "le", "les", "te") { #"se"    apertium sí: "te",
            my $stemhere = $form;
            $stemhere =~ s/á$/a/;
            $stemhere =~ s/é$/e/;
            $stemhere =~ s/í$/i/;
            if ($key =~ /^(os)$/ && $lemma !~ /^ir$/)  {$stemhere =~ s/i$/í/;}  #partíos
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }
       
        foreach my $key1 ("me",  "se", "nos", "os" , "te") {  # apertium sí: "te",
            foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") { # le, les infreqüents?
                if ($key1 =~ /^se$/ && $key2 =~ /^les?$/) {next;}
                my $stemhere = $stem;
                if ($key1 =~ /^os$/ && $lemma !~ /^ir$/) {$stemhere =~ s/d$//;}
                $result .= "$stemhere$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
=pod         
        foreach my $key1 ("os") {  
            foreach my $key2 ("me", "nos") {
                my $stemhere = $stem;
                if ($key1 =~ /^(os)$/ && $lemma !~ /^ir$/) {$stemhere =~ s/d$//;}
                $result .= "$stemhere$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
            }   
        }
        #te+
        foreach my $key3 ("me", "nos") {
            $result .= "${stem}te$key3 $lemma $postag+".$pronouns{"te"}."$jointags$pronouns{$key3}\n"  
        }  
=cut
    } elsif ($postag =~ /V.M.2S./) { #canta, teme, parte, peina, renueva, pinta, piensa, actúa # més: haz, pon, sal, di ...
        #desáhuciala
        if    ($stem !~ /[áéíóú]/) { $stem =~ s/a(huci[ae]n?)$/á$1/; }
        if    ($stem !~ /[áéíóú]/) { $stem =~ s/a([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/á$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/e([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/é$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/o([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ó$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/au([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/áu$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/eu([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/éu$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/ei([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/éi$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/ai([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ái$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/oi([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ói$1/; }
        #lícuala, averíguala
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^eaoéáó])i([^aeiouáéíóú]*([gqc][uü])[ae]n?)$/$1í$2/; }
        #írguela
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^i([^aeiouáéíóú]*([gqc][uü])[ae]n?)$/í$1/; }
        #anúnciala
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^aeoéáó])u([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/$1ú$2/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^eaoéáó])i([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/$1í$2/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^u([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ú$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^i([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/í$1/; }
        

        foreach my $key ("me", "nos", "te", "lo", "los" , "la", "las" , "le", "les") { 
            if ($stem =~ /l$/ && $key =~ /^l/) { next;}  #exception: salle
            my $stemhere = $stem;
            # Exception: -> estame 
            $stemhere =~ s/é$/e/;
            $stemhere =~ s/én$/en/;
            $stemhere =~ s/á$/a/;
            $stemhere =~ s/án$/an/;
            $stemhere =~ s/í$/i/;
            $stemhere =~ s/ín$/in/;
            $stemhere =~ s/ó$/o/;
            $stemhere =~ s/ón$/on/;
            $stemhere =~ s/ú$/u/;
            $stemhere =~ s/ún$/un/;
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }
        
        if ($stem !~ /[áéíóú]/) {
            $stem =~ s/az$/áz/;
            $stem =~ s/on$/ón/;
            $stem =~ s/i$/í/;
            $stem =~ s/^da$/dá/;
            $stem =~ s/e$/é/;
            $stem =~ s/en$/én/;
        }

        if ($stem !~ /l$/) {
            if ($stem =~ /^$form$/ && $form !~ /[áéíóú]/) {print "POSSIBLE ERROR EN: $form\n"};
            foreach my $key1 ("me", "te", "se", "nos", ) { 
                foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") {
                    if ($key1 =~ /^se$/ && $key2 =~ /^les?$/) {next;}
                    $result .= "$stem$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
                }   
            }
            #te+
            foreach my $key3 ("me", "nos") {
                $result .= "${stem}te$key3 $lemma $postag$jointags".$pronouns{"te"}."$jointags$pronouns{$key3}\n"  
            }    
        }
    } elsif ($postag =~ /V.M.3[SP]./) { 
        #cante, tema, parta, peine, renueve, pinte, piense, actúe # més: haga, ponga, salga, diga ...
        #canten, teman, partan, peinen, renueven, pinten, piensen, actúen
        #desáhuciala
        if    ($stem !~ /[áéíóú]/) { $stem =~ s/a(huci[ae]n?)$/á$1/; }
        if    ($stem !~ /[áéíóú]/) { $stem =~ s/a([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/á$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/e([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/é$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/o([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ó$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/au([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/áu$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/eu([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/éu$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/ei([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/éi$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/ai([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ái$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/oi([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ói$1/; }
        #lícuala, averíguala
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^eaoéáó])i([^aeiouáéíóú]*([gqc][uü])[ae]n?)$/$1í$2/; }
        #írguela
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^i([^aeiouáéíóú]*([gqc][uü])[ae]n?)$/í$1/; }
        #anúnciala
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^aeoéáó])u([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/$1ú$2/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/([^eaoéáó])i([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/$1í$2/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^u([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/ú$1/; }
        if ($stem !~ /[áéíóú]/) { $stem =~ s/^i([^aeiouáéíóú]*([qg][uü])?[iu]?[ae]n?)$/í$1/; }

        foreach my $key ("se", "me", "nos", "os", "te", "lo", "los" , "la", "las" , "le", "les") { 
            if ($stem =~ /l$/ && $key =~ /^l/) { next;}
            my $stemhere = $stem;
            # Exception: dé -> deme, dele, estelo, estenla
            $stemhere =~ s/é$/e/;
            $stemhere =~ s/én$/en/;
            $stemhere =~ s/á$/a/;
            $stemhere =~ s/án$/an/;
            $stemhere =~ s/í$/i/;
            $stemhere =~ s/ín$/in/;
            $stemhere =~ s/ó$/o/;
            $stemhere =~ s/ón$/on/;
            $stemhere =~ s/ú$/u/;
            $stemhere =~ s/ún$/un/;
            
            $result .= "$stemhere$key $lemma $postag$jointags$pronouns{$key}\n"
        }

        $stem =~ s/^den$/dén/;
        if ($stem =~ /^$form$/ && $form !~ /[áéíóú]/) {print "POSSIBLE ERROR EN: $form\n"};

        if ($stem !~ /l$/) {
            foreach my $key1 ("me", "te", "se", "nos", "os") { 
                foreach my $key2 ("lo", "los" , "la", "las" , "le", "les") {
                    $result .= "$stem$key1$key2 $lemma $postag$jointags$pronouns{$key1}$jointags$pronouns{$key2}\n"
                }   
            }
            #se+
            foreach my $key3 ("me", "te", "nos", "os") {
                $result .= "${stem}se$key3 $lemma $postag$jointags".$pronouns{"se"}."$jointags$pronouns{$key3}\n"  
            }  
            #te+
            foreach my $key3 ("me", "nos") {
                $result .= "${stem}te$key3 $lemma $postag$jointags".$pronouns{"te"}."$jointags$pronouns{$key3}\n"  
            }    
        }
    }

    # Formes no generades que Apertium sí que té: cantadte, cantádtela, cantádtelas, 
    # cantádtele, cantádteles, cantádtelo, cantádtelos, cantándoosme, cantándoosnos, 
    # cantárosme, cantárosnos, cantémoosme, cantémoosnos, cántenosme, cántenosnos, 
    # cánteosme, cánteosnos

    return $result;

}

1;
