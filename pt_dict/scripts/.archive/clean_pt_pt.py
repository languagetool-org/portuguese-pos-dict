from pt_dict.constants import LATIN_1_ENCODING
from pt_dict.variants.variant import PT_PT_90, PT_PT_45


def main():
    pt_vars = [PT_PT_90, PT_PT_45]
    for var in pt_vars:
        for filepath in [var.dic(), var.compounds()]:
            all_lines = []
            with open(filepath, 'r', encoding=LATIN_1_ENCODING) as dic_file:
                for line in dic_file.read().split("\n"):
                    all_lines.append(line.split("\t")[0])
            with open(filepath, 'w', encoding=LATIN_1_ENCODING) as dic_file:
                dic_file.write("\n".join(all_lines))


if __name__ == '__main__':
    main()
