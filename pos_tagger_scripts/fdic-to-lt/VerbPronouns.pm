package VerbPronouns;

print "VerbPronouns module loaded\n";

sub future_subjunctive {
    my ($form, $lemma, $postag, $pronoun) = @_;

    # List of specific irregular verbs
    my $irregular_verbs_regex = qr/(souber|couber|trouxer|fizer|disser)$/;

    # Apply accent rules for specific irregular verbs and standard rules for others
    if ($pronoun =~ /^(o|os|a|as)$/) {
        if ($form =~ /ar$/) {
            $form =~ s/ar$/á/;
        } elsif ($form =~ $irregular_verbs_regex) {
            $form =~ s/er$/é/;
        } elsif ($form =~ /er$/) {
            $form =~ s/er$/ê/;
        } elsif ($form =~ /or$/) {
            $form =~ s/or$/ô/;
        } elsif ($form =~ /ir$/) {
            $form =~ s/ir$/i/;  # No accent for -ir verbs
        }
    }

    return $form . "-" . $pronoun;
}

sub infinitive {
    my ($form, $pronoun) = @_;  # 'form' is the infinitive verb, 'pronoun' is the clitic pronoun

    # Handling exceptions with pronouns "o", "os", "a", "as"
    if ($pronoun =~ /^(o|os|a|as)$/) {
        if ($form =~ /ar$/) {
            $form =~ s/ar$/á/;  # Replacing 'ar' with 'á' for -ar verbs
        } elsif ($form =~ /er$/) {
            $form =~ s/er$/ê/;  # Replacing 'er' with 'ê' for -er verbs
        } elsif ($form =~ /or$/) {
            $form =~ s/or$/ô/;  # Replacing 'or' with 'ô' for -or verbs
        } elsif ($form =~ /ir$/) {
            $form =~ s/ir$/i/;  # Replacing 'ir' with 'i' for -ir verbs, no accent
        }
        return $form . "-" . $pronoun;  # Appending the pronoun with a hyphen
    }

    # For all other cases, simply append the pronoun with a hyphen
    return $form . "-" . $pronoun;
}

1;
