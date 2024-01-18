package Flexio;
use strict;
use warnings;
use utf8;
use Text::Unaccent::PurePerl qw(unac_string);

our $carac="[ôõãÅ₂²³a-zA-ZûêàéèíòóúïüäöîâëÄÖÀÈÉÍÒÓÚÏÜÎÂËçÇñÑáå·0-9'\-:]";
our $number_exceptions="^(?i)(L2|P[345]|MP[34]|A[345]|goma-2|4x4|Covid-19|COVID-19|covid-19|SARS-CoV-2|N95|FFP2|Z80|x64|x86)\$";

my $tag_joiner = ":";

our %pronouns;
$pronouns{"o"}="PP3MSA00";
$pronouns{"os"}="PP3MPA00";
$pronouns{"a"}="PP3FSA00";
$pronouns{"as"}="PP3FPA00";
$pronouns{"lhe"}="PP3CSD00";
$pronouns{"lhes"}="PP3CPD00";
$pronouns{"me"}="PP1CSO00";
$pronouns{"te"}="PP2CSO00";
$pronouns{"se"}="PP3CNO00";
$pronouns{"nos"}="PP1CPO00";
$pronouns{"vos"}="PP2CPO00";
$pronouns{"no-lo"}="PP1CPO00:PP3MSA00";
$pronouns{"no-los"}="PP1CPO00:PP3MPA00";
$pronouns{"no-la"}="PP1CPO00:PP3FSA00";
$pronouns{"no-las"}="PP1CPO00:PP3FPA00";

# These rare forms only appear with unelided verbs, we can rely on the current tokenisation logic
# to identify them; we'll take the risk with mesoclitic forms... 'dar-lho-ei'? come on
# $pronouns{"lha"}="PP3CSD00:PP3FSA00";
# $pronouns{"lhas"}="PP3CSD00:PP3FPA00";
# $pronouns{"lho"}="PP3CSD00:PP3MSA00";
# $pronouns{"lhos"}="PP3CSD00:PP3MPA00";
# $pronouns{"ma"}="PP1CSO00:PP3FSA00";
# $pronouns{"mas"}="PP1CSO00:PP3FPA00";
# $pronouns{"mo"}="PP1CSO00:PP3MSA00";
# $pronouns{"mos"}="PP1CSO00:PP3MPA00";
# $pronouns{"ta"}="PP2CSO00:PP3FSA00";
# $pronouns{"tas"}="PP2CSO00:PP3FPA00";
# $pronouns{"to"}="PP2CSO00:PP3MSA00";
# $pronouns{"tos"}="PP2CSO00:PP3MPA00";
# $pronouns{"vo-lo"}="PP2CPO00:PP3MSA00";
# $pronouns{"vo-los"}="PP2CPO00:PP3MPA00";
# $pronouns{"vo-la"}="PP2CPO00:PP3FSA00";
# $pronouns{"vo-las"}="PP2CPO00:PP3FPA00";

my @always_elision_pronouns = ("o", "os", "a", "as");
my @never_elision_pronouns = ("lhe", "lhes", "me", "te", "se", "vos",
                              # "vo-lo", "vo-los", "vo-la", "vo-las",
                              # "lho", "lhos", "lha", "lhas", "mo", "mos", "ta", "tas", "to", "tos", "ma", "mas"
                              );
my @mos_elision_pronouns = ("nos", "no-lo", "no-los", "no-la", "no-las");
my @rarely_elision_pronouns = @never_elision_pronouns;
push(@rarely_elision_pronouns, @mos_elision_pronouns);

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

sub r_elision {
    my $form = $_[0];
    my $elided_form = $form;
    if ($form =~ /(fizer|trouxer|[sc]ouber|quiser|puser|tiver|vier|estiver|disser)$/ || $form =~ /^(der|(re)?quer)$/) {
        $elided_form =~ s/er$/é/;
        return $elided_form;
    }
    if ($form =~ /er$/) {
        $elided_form =~ s/er$/ê/;
        return $elided_form;
    }
    if ($form =~ /ar$/) {
        $elided_form =~ s/ar$/á/;
        return $elided_form;
    }
    if ($form =~ /[aeo]ir$/) {
        $elided_form =~ s/ir$/í/;
        return $elided_form;
    }
    if ($form =~ /ir$/) {
        $elided_form =~ s/ir$/i/;
        return $elided_form;
    }
    if ($form =~ /[oô]r$/) {
        $elided_form =~ s/[oô]r$/ô/;
        return $elided_form;
    }
}

sub z_elision {
    my $form = $_[0];
    my $elided_form = $form;
    if ($form =~ /[ui]z$/) {
        $elided_form =~ s/z$//;
        return $elided_form;
    }
    if ($form =~ /ez$/) {
        $elided_form =~ s/ez$/ê/;
        return $elided_form;
    }
    if ($form =~ /az$/) {
        $elided_form =~ s/az$/á/;
        return $elided_form;
    }
}

sub s_elision {
    my $elided_form = $_[0];
    $elided_form =~ s/s$//;
    return $elided_form;
}

sub mesoclitic_form {
    my $form = $_[0];
    my $pron_form = $_[1];
    my $elide = $_[2];
    if ($form =~ /^(.+r)([^r]+)$/) {
        my $stem = $1;
        if ($elide == 1) {
            $stem = r_elision($stem);
        }
        my $ending = $2;
        return "$stem-$pron_form-$ending";
    }
}

sub verb_pronouns {
    # TODO: pronoun sequences, e.g. "mos", "lha", "vo-lo"
    my $form=$_[0];
    my $lemma=$_[1];
    my $postag=$_[2];
    my $result = "";

    # Perl is stupid and doesn't have closures, so we have to do this
    my $add_enclitic_to_result = sub {
        my $pron_form = $_[0];
        my $stem = $_[1];
        my $pron_tag = $_[2];
        $result .= "$stem-$pron_form\t$lemma\t$postag$tag_joiner$pron_tag\n"
    };
    my $add_mesoclitic_to_result = sub {
        my $pron_form = $_[0];
        my $stem = $_[1];
        my $pron_tag = $_[2];
        my $elide = $_[3];
        $result .= mesoclitic_form($stem, $pron_form, $elide) . "\t$lemma\t$postag$tag_joiner$pron_tag\n"
    };

    if ($form =~ /r$/) {
        foreach my $pron (@rarely_elision_pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_enclitic_to_result->("l$pron", r_elision($form), $pronouns{$pron});
        }
    } elsif ($postag =~ /^V.I[CF].+/) {
        foreach my $pron (@rarely_elision_pronouns) {
            $add_mesoclitic_to_result->($pron, $form, $pronouns{$pron}, 0);
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_mesoclitic_to_result->("l$pron", $form, $pronouns{$pron}, 1);
        }
    } elsif ($form =~ /(m|ão|õe)$/) {
        foreach my $pron (@rarely_elision_pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_enclitic_to_result->("n$pron", $form, $pronouns{$pron});
        }
    } elsif ($form =~ /mos$/) {
        foreach my $pron (@never_elision_pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_enclitic_to_result->("l$pron", s_elision($form), $pronouns{$pron});
        }
        foreach my $pron (@mos_elision_pronouns) {
            $add_enclitic_to_result->($pron, s_elision($form), $pronouns{$pron});
        }
        $add_enclitic_to_result->("nos", s_elision($form), $pronouns{"nos"});
    } elsif ($form =~ /[aeiouáéêóôíú]s$/ && $postag !~ /^V.P.+/) {
        foreach my $pron (@rarely_elision_pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_enclitic_to_result->("l$pron", s_elision($form), $pronouns{$pron});
        }
    } elsif ($form =~ /[aeiu]z$/) {
        foreach my $pron (@rarely_elision_pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
        foreach my $pron (@always_elision_pronouns) {
            $add_enclitic_to_result->("l$pron", z_elision($form), $pronouns{$pron});
        }
    } elsif ($form =~ /[aeiouáéêóôíú]$/ && $postag !~ /^V.P.+/) {
        foreach my $pron (keys %pronouns) {
            $add_enclitic_to_result->($pron, $form, $pronouns{$pron});
        }
    }
    return $result;
}

# lmao
1;
