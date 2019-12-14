
class TestParser(Parser):

    @memoise
    def atom(self):
        name = self.expect('NAME')
        if name:
            return name
        number = self.expect('NUMBER')
        if number:
            return number
        return None

    @memoise
    def atom_list(self):
        atom = self.atom()
        if atom:
            atom_list = self.atom_list()
            if atom_list:
                return Node('atom_list', [atom] + atom_list.children)
            return Node('atom_list', [atom])
        return None

    @memoise
    def list(self):
        pos = self.mark()
        lbrack = self.expect('LSQUARE')
        if lbrack:
            atom_list = self.atom_list()
            if atom_list:
                rbrack = self.expect('RSQUARE')
                if rbrack:
                    return Node('list', atom_list.children)
        self.reset(pos)
        return None

    @memoise
    def let_stmt(self):
        pos = self.mark()
        target = self.expect('NAME')
        if target:
            op = self.expect('ASSIGN')
            if op:
                expr = self.expr()
                if expr and self.expect('NEWLINE'):
                    return Node('statement', [target, expr])
        self.reset(pos)
        return None

    @memoise_left_recursive
    def expr(self):

        list_ = self.list()
        if list_:
            return list_

        pos_start = self.mark()
        lhs = self.expr()
        if lhs:
            pos_op = self.mark()
            for op_name in ['MUL', 'ADD']:
                op = self.expect(op_name)
                if op:
                    rhs = self.expr()
                    if rhs:
                        return Node('binop', [lhs, op, rhs])
                self.reset(pos_op)
        self.reset(pos_start)
