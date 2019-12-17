import re
import sys

from pegparsing import Token


terminal_regex = re.compile(r'[A-Z_]+')
nonterminal_regex = re.compile(r'[a-z_]+')
string_regex = re.compile(r'(\'[^\']*\')|(\"[^\"]*\")')
codeblock_regex = re.compile(r'{[^}]*}')
symbols = set(':;|@')
ignore = set(' \t\f\v\r\n')


def string_transform(string):
    return string[1:-1]


def codeblock_transform(string):
    return string[1:-1].strip().replace('\n', ' ')


def tokenise(data):
    line, col = 1, 0
    pos = 0
    while pos < len(data):
        char = data[pos]

        if char in ignore:
            if char == '\n':
                line, col = line + 1, 0
            col += 1
            pos += 1
            continue

        if char in symbols:
            yield Token(char, char, line, col)
            col += 1
            pos += 1
            continue

        for regex, token_type, transform in (
                (terminal_regex, 'TERMINAL', None),
                (nonterminal_regex, 'NONTERMINAL', None),
                (string_regex, 'STRING', string_transform),
                (codeblock_regex, 'CODEBLOCK', codeblock_transform)
        ):
            if match := regex.match(data, pos):
                endpos = match.span()[1]
                string = data[pos:endpos]
                if transform:
                    string = transform(string)
                yield Token(token_type, string, line, col)
                col += endpos - pos
                pos = endpos
                break

        else:
            raise ValueError(f'Unrecognised character "{char}" '
                             f'at line {line}, col {col}')

    yield Token('ENDMARKER', '', line, col)


if __name__ == '__main__':

    with open(sys.argv[1], 'r') as f:
        tokens = tokenise(f.read())
    for t in tokens:
        print(t)
