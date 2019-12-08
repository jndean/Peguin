import re
from rply import Token


nonterminal_regex = re.compile(r'[a-z_]+')
terminal_regex = re.compile(r'[A-Z]+')
symbols = {':': 'COLON',
           ';': 'SEMI',
           '|': 'OR'}
ignore = set(' \t\f\v\r\n')


def lex(data):
    line, col = 1, 0
    pos = 0
    while pos < len(data):
        char = data[pos]
        if char in ignore:
            if char == '\n':
                line, col = line + 1, 0
            pos += 1
            continue

        if char in symbols:
            yield Token(symbols[char], char)  # , (line, col))
            col += 1
            pos += 1
            continue

        terminal_match = terminal_regex.match(data, pos)
        if terminal_match:
            endpos = terminal_match.span()[1]
            string = data[pos:endpos]
            yield Token('TERMINAL', string)  # , (line, col))
            col += endpos - pos
            pos = endpos
            continue

        nonterminal_match = nonterminal_regex.match(data, pos)
        if nonterminal_match:
            endpos = nonterminal_match.span()[1]
            string = data[pos:endpos]
            yield Token('NONTERMINAL', string)  # , (line, col))
            col += endpos - pos
            pos = endpos
            continue

        raise ValueError(f'Unrecognised character: "{char}"')


if __name__ == '__main__':
    tokens = lex("""
        rule : NONTERMINAL COLON options SEMI ;
        options : token_list OR options | token_list ;
        token_list : token token_list | token ;
        token : TERMINAL | NONTERMINAL ;
    """)

    for t in tokens:
        print(t)
