import re
from typing import List

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.dicts.hunspell import HunspellDict
from pt_dict.variants.variant import DIC_VARIANTS


def main():
    for var in DIC_VARIANTS:
        # must be list so we maintain the order
        write_lines = []
        unique_lines = set()
        all_lemmata = set()

        lemma_to_line_mapping: dict[str: List[str]] = dict()
        with open(var.compounds(), 'r', encoding=LATIN_1_ENCODING) as dic_file:
            all_lines = dic_file.read().split("\n")[1:]
            for line in all_lines:
                lemma_match = HunspellDict.pattern.match(line)
                if lemma_match:
                    lemma = lemma_match.group(1)
                    if lemma in lemma_to_line_mapping.keys():
                        lemma_to_line_mapping[lemma].append(line)
                    else:
                        lemma_to_line_mapping[lemma] = [line]
                    all_lemmata.add(lemma)
                    if line not in unique_lines:
                        unique_lines.add(line)
                        write_lines.append(line)
        print(var)
        total_all_lines = len(all_lines)
        total_unique_lines = len(unique_lines)
        print(f"total - unique = duplicated lines || {total_all_lines} - {total_unique_lines} = {total_all_lines - total_unique_lines}")

        lemmata_with_multiple_lines = set(filter(lambda l: len(lemma_to_line_mapping[l]) > 1, lemma_to_line_mapping.keys()))
        print(f"duplicated lemmata: {len(lemmata_with_multiple_lines)}")

        lemmata_with_multiple_unique_lines = set(filter(lambda l: len(set(lemma_to_line_mapping[l])) > 1, lemma_to_line_mapping.keys()))
        print(f"duplicated lemmata with multiple unique lines: {len(lemmata_with_multiple_unique_lines)}")
        print(sorted(lemmata_with_multiple_unique_lines))

        tag_pattern = re.compile("/(.*)$")
        for lemma, lines in lemma_to_line_mapping.items():
            if len(set(lines)) < 2:
                continue
            tags = set()
            for line in lines:
                try:
                    write_lines.remove(line)
                except:
                    pass
                tag_match = tag_pattern.search(line)
                if tag_match:
                    tag = set(tag_match.group(1))
                    tags.update(tag)
            if len(tags) == 0:
                new_line = lemma
            else:
                new_line = f"{lemma}/{''.join(sorted(tags))}"
            write_lines.append(new_line)
        with open(var.compounds(), 'w', encoding=LATIN_1_ENCODING) as dic_file:
            dic_file.write(str(len(write_lines)) + "\n")
            dic_file.write("\n".join(write_lines))


if __name__ == '__main__':
    main()
