"""Extract differences between PT varieties."""
import re


# Define a set to store lemmas
lemmata = set()

# Define output files
EXCLUDING_FILENAME = "br-pt_excluding.txt"
RECOMMEND_FILENAME = "br-pt_recommend-BR.txt"
UNCERTAIN_FILENAME = "br-pt_uncertain.txt"

# Define sets to store lemmas that match specific patterns
excluding_set = set()
recommend_set = set()
uncertain_set = set()

OUTPUT_SET_MAPPING = [
    (EXCLUDING_FILENAME, excluding_set),
    (RECOMMEND_FILENAME, recommend_set),
    (UNCERTAIN_FILENAME, uncertain_set)
]

FILES_TO_PROCESS = {
    "adjectives-fdic.txt", "nouns-fdic.txt", "verbs-fdic.txt",
    "adverbs-lt.txt", "adv_mente-lt.txt", "propernouns-lt.txt",
    "resta-lt.txt"
}

# Set of tuples, where the first element is to be replaced with the second
# The third element is the specific set that this equivalency belongs to
# Though this is definitely not the whole story
GRAPHEME_EQUIVALENCIES = [
    ('ê', 'é', excluding_set),
    ('ô', 'ó', excluding_set),
    ('pt', 't', recommend_set),
    ('cç', 'ç', recommend_set),
    ('ct', 't', uncertain_set),
    ('pç', 'ç', uncertain_set),
]


def process_file(filename: str):
    """Define a function to process a file and collect lemmata."""
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = re.match(r'^([^# =]+)', line)
            if match:
                lemmata.add(match.group(1))


for file_to_process in FILES_TO_PROCESS:
    process_file(f"../src-dict/{file_to_process}")

# Process lemmas and categorize them
for lemma in sorted(lemmata):
    for equivalency in GRAPHEME_EQUIVALENCIES:
        if equivalency[0] in lemma:
            new_lemma = lemma.replace(*equivalency[0:2])
            if new_lemma in lemmata:
                equivalency[2].add("=".join([lemma, new_lemma]))

# Write results to output files
for output_pair in OUTPUT_SET_MAPPING:
    with open(output_pair[0], 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(sorted(output_pair[1])))
