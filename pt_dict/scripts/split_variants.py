"""This module makes sure the pt_BR_90, pt_PT_45, and pt_PT_90 hunspell dictionaries contain appropriate forms."""


from pt_dict.constants import TWO_WAY_ALTERNATIONS_FILEPATH


def split_dialects():
    """Perform the BR <=> PT alternation."""

