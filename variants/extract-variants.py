import re

# Define a function to process a file and collect lemmas
def process_file(filename, lemmas):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = re.match(r'^([^# =]+)', line)
            if match:
                lemma = match.group(1)
                lemmas.add(lemma)

# Define a set to store lemmas
lemmas = set()

# Process the first set of files
files = ["adjectives-fdic.txt", "nouns-fdic.txt", "verbs-fdic.txt"]
for file in files:
    filename = f"../src-dict/{file}"
    process_file(filename, lemmas)

# Process the second set of files
files = ["adverbs-lt.txt", "adv_mente-lt.txt", "propernouns-lt.txt", "resta-lt.txt"]
for file in files:
    filename = f"../src-dict/{file}"
    process_file(filename, lemmas)

# Define output files
output_file1 = "br-pt_excluding.txt"
output_file2 = "br-pt_recommend-BR.txt"
output_file3 = "br-pt_uncertain.txt"

# Define sets to store lemmas that match specific patterns
exclude_set1 = set()
recommend_set = set()
uncertain_set = set()

# Process lemmas and categorize them
for lemma in sorted(lemmas):
    if 'ê' in lemma:
        lemma2 = lemma.replace('ê', 'é')
        if lemma2 in lemmas:
            exclude_set1.add(f"{lemma}={lemma2}")

    if 'ô' in lemma:
        lemma2 = lemma.replace('ô', 'ó')
        if lemma2 in lemmas:
            exclude_set1.add(f"{lemma}={lemma2}")

    if 'pt' in lemma:
        lemma2 = lemma.replace('pt', 't')
        if lemma2 in lemmas:
            recommend_set.add(f"{lemma2}={lemma}")

    if 'cç' in lemma:
        lemma2 = lemma.replace('cç', 'ç')
        if lemma2 in lemmas:
            recommend_set.add(f"{lemma2}={lemma}")

    if 'ct' in lemma:
        lemma2 = lemma.replace('ct', 't')
        if lemma2 in lemmas:
            uncertain_set.add(f"{lemma2}={lemma}")

    if 'pç' in lemma:
        lemma2 = lemma.replace('pç', 'ç')
        if lemma2 in lemmas:
            uncertain_set.add(f"{lemma}={lemma2}")

# Write results to output files
with open(output_file1, 'w', encoding='utf-8') as ofh:
    ofh.write('\n'.join(sorted(exclude_set1)))

with open(output_file2, 'w', encoding='utf-8') as ofh2:
    ofh2.write('\n'.join(sorted(recommend_set)))

with open(output_file3, 'w', encoding='utf-8') as ofh3:
    ofh3.write('\n'.join(sorted(uncertain_set)))
