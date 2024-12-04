import unicodedata

def split_accented_char(char):
    if char in 'çÇ':
        return char.lower()

    decomposed = unicodedata.normalize('NFD', char)

    replacements = {
        '\u0301': '\u00B4',  # Combining acute accent -> ´ (U+00B4)
        '\u0302': '\u005E',  # Combining circumflex accent -> ^ (U+005E)
        '\u0303': '\u007E',  # Combining tilde -> ~ (U+007E)
    }

    result = ""

    for c in decomposed:
        isDiacritics = unicodedata.category(c) == 'Mn'
        if isDiacritics:
            if c not in replacements:
                continue
            result += replacements[c]
        else:
            result += c.lower()

    return result[::-1]


def main():
    input_file = "Final Project\Text\en-en.txt"
    output_file = "EN-Preprocessed-file"

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            for char in line:
                char = split_accented_char(char)
                outfile.write(f'{char}')
        outfile.write("\n")

    print(f"Results have been written to {output_file}")

main()
