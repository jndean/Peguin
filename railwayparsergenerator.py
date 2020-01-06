from metatokeniser import tokenise as metatokenise
from parsergenerator import ParserGenerator, Token as MetaToken
from railwaylexer import tokenise


class Token:
    __slots__ = ['type', 'string', 'line', 'col', 'first_set']

    def __init__(self, type, string, line, col):
        self.type = type
        self.string = string
        self.line = line
        self.col = col
        self.first_set = {string}

    def __repr__(self):
        return self.string

    def codegen(self, rules):
        pass


class Binop:
    __slots__ = ['lhs', 'op', 'rhs']

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return f'Binop({self.lhs} {self.op} {self.rhs})'


class Let:
    __slots__ = ['lhs', 'rhs']

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f'let {self.lhs} = {self.rhs}'


if __name__ == '__main__':

    # Generate the railway parser #
    with open('Grammars/railway.peg', 'r') as f:
        tokens = metatokenise(f.read(), TokenClass=MetaToken)
    parser_generator = ParserGenerator(tokens)
    grammar = parser_generator.rule_grammar()
    railway_parser_code = grammar.codegen('RailwayParser')
    with open('railwayparser.py', 'w') as f:
        f.write(railway_parser_code)

    # Temporary tests of the generated parser #
    from railwayparser import RailwayParser
    with open('tmp.rail', 'r') as f:
        tokens = tokenise(f.read(), TokenClass=Token)
    parser = RailwayParser(tokens)
    rule = parser.rule_let_stmt()
    print(rule)