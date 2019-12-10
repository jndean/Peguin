import re
from rply import Token


name_regex = re.compile(r'[a-zA-Z_]+')
string_regex = re.compile(r'(\'[^\']*\')|(\"[^\"]*\")')
action_regex = re.compile(r'{[^}]*}')
symbols = set(':;|')
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
            yield Token(char, char)  # , (line, col))
            col += 1
            pos += 1
            continue

        for regex, token_type in ((name_regex, 'NAME'),
                                  (string_regex, 'STRING'),
                                  (action_regex, 'ACTION')):

            match = regex.match(data, pos)
            if match:
                endpos = match.span()[1]
                string = data[pos:endpos]
                yield Token(token_type, string)  # , (line, col))
                col += endpos - pos
                pos = endpos
                break

        else:
            raise ValueError(f'Unrecognised character: "{char}"')

    yield Token('ENDMARKER', '')


if __name__ == '__main__':
    tokens = lex("""
        rule : NAME ':' options ';' ;
        options : option '|' options | option ;
        option : item_list ACTION | item_list ;
        item_list : item item_list | item ;
        item : NAME | STRING ;
    """)

    for t in tokens:
        print(t)
