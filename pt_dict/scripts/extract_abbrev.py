import re

from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.variants.variant import PT_BR


def main():
    pattern = re.compile("^((?:\\w+\\.)+(?:\\w+)?)(?:/|$)")
    new_lines = []
    abbrevs = []
    with open(PT_BR.dic(), 'r', encoding=LATIN_1_ENCODING) as br_file:
        lines = br_file.read().split("\n")
        for line in lines:
            match = pattern.match(line)
            if match:
                abbrev = match.group(1)
                print(abbrev)
                abbrevs.append(abbrev)
            else:
                new_lines.append(line)
    with open("abbreviations.txt", 'w') as abbrev_file:
        abbrev_file.write("\n".join(abbrevs))
        print("total abbreviations:", len(abbrevs))
    with open(PT_BR.dic(), 'w', encoding=LATIN_1_ENCODING) as br_file:
        br_file.write("\n".join(new_lines))


if __name__ == "__main__":
    main()
