from metatokeniser import tokenise as metatokenise
from parsergenerator import ParserGenerator, Token as MetaToken
from railwaytokeniser import tokenise


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


class ThreadID:
    __slots__ = []

    def __repr__(self):
        return 'TID'


class NumThreads:
    __slots__ = []

    def __repr__(self):
        return '#TID'


class Lookup:
    __slots__= ['name', 'index']

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        if self.index:
            return f'{self.name}[{"][".join(self.index)}]'
        return self.name


class Length:
    __slots__ = ['lookup']

    def __init__(self, lookup):
        self.lookup = lookup

    def __repr__(self):
        return f'#{repr(self.lookup)}'


class Binop:
    __slots__ = ['lhs', 'op', 'rhs']

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return f'Binop({self.lhs} {self.op} {self.rhs})'


class Uniop:
    __slots__ = ['op', 'expr']

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'Uniop({self.op}{self.expr})'


class ArrayLiteral:
    __slots__ = ['items']

    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return repr(self.items)


class ArrayRange:
    __slots__ = ['start', 'stop', 'step']

    def __init__(self, start, stop, step=None):
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        by_str = '' if self.step is None else f' by {self.step}'
        return f'[{self.start} to {self.stop}{by_str}]'


class ArrayTensor:
    __slots__ = ['fill_expr', 'dims_expr']

    def __init__(self, fill_expr, dims_expr):
        self.fill_expr = fill_expr
        self.dims_expr = dims_expr

    def __repr__(self):
        return f'[{self.fill_expr} tensor {self.dims_expr}]'


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