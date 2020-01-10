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
            return f'{self.name}[{"][".join(repr(i) for i in self.index)}]'
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
        assignment = f' = {self.rhs}' if self.rhs is not None else' '
        return f'let {self.lhs}{assignment}'


class Unlet:
    __slots__ = ['lhs', 'rhs']

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        assignment = f' = {self.rhs}' if self.rhs is not None else' '
        return f'unlet {self.lhs}{assignment}'


class Promote:
    __slots__ = ['src_name', 'dst_name']

    def __init__(self, src_name, dst_name):
        self.src_name = src_name
        self.dst_name = dst_name

    def __repr__(self):
        return f'promote {self.src_name} => {self.dst_name}'


class Push:
    __slots__ = ['src_lookup', 'dst_lookup']

    def __init__(self, src_lookup, dst_lookup):
        self.src_lookup = src_lookup
        self.dst_lookup = dst_lookup

    def __repr__(self):
        return f'push {self.src_lookup} => {self.dst_lookup}'


class Pop:
    __slots__ = ['src_lookup', 'dst_lookup']

    def __init__(self, src_lookup, dst_lookup):
        self.src_lookup = src_lookup
        self.dst_lookup = dst_lookup

    def __repr__(self):
        return f'pop {self.src_lookup} => {self.dst_lookup}'


class Swap:
    __slots__ = ['lhs', 'rhs']

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f'swap {self.lhs} <=> {self.rhs}'


class If:
    __slots__ = ['enter_expr', 'lines', 'else_lines', 'exit_expr']

    def __init__(self, enter_expr, lines, else_lines, exit_expr):
        self.enter_expr = enter_expr
        self.lines = lines
        self.else_lines = else_lines
        self.exit_expr = exit_expr

    def __repr__(self):
        lines = [f'if ({self.enter_expr})'] + [repr(l) for l in self.lines]
        if self.else_lines is not None:
            lines += ['else'] + [repr(l) for l in self.else_lines]
        lines.append(f'fi ({self.exit_expr})')
        return '\n'.join(lines)


class Loop:
    __slots__ = ['forward_condition', 'lines', 'backward_condition']

    def __init__(self, forward_condition, lines, backward_condition):
        self.forward_condition = forward_condition
        self.lines = lines
        self.backward_condition = backward_condition

    def __repr__(self):
        return '\n'.join([f'loop ({self.forward_condition})'] +
                         [repr(l) for l in self.lines] +
                         [f'pool ({self.backward_condition})'])


class For:
    __slots__ = ['lookup', 'iterator', 'lines']

    def __init__(self, lookup, iterator, lines):
        self.lookup = lookup
        self.iterator = iterator
        self.lines = lines

    def __repr__(self):
        return '\n'.join([f'for ({self.lookup} in {self.iterator})'] +
                         [repr(l) for l in self.lines] +
                         ['rof'])


class Modop:
    __slots__ = ['lookup', 'op', 'expr']

    def __init__(self, lookup, op, expr,):
        self.lookup = lookup
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'{self.lookup} {self.op} {self.expr}'


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
    rule = parser.rule_program()
    print(rule)