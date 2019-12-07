#!/usr/bin/env python3

from collections import namedtuple
import sys

from newlexer import lex


Node = namedtuple("Node", ["type", "children"])


class Tokeniser:
    def __init__(self, string):
        self.gen = lex(string)
        self.tokens = []
        self.pos = 0

    def mark(self):
        return self.pos

    def reset(self, pos):
        self.pos = pos

    def get_token(self):
        token = self.peek_token()
        self.pos += 1
        return token

    def peek_token(self):
        if self.pos == len(self.tokens):
            self.tokens.append(next(self.gen))
        return self.tokens[self.pos]


class Parser:
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.memos = {}

    def mark(self):
        return self.tokeniser.mark()

    def reset(self, pos):
        self.tokeniser.reset(pos)

    def expect(self, arg):
        token = self.tokeniser.peek_token()
        if token.gettokentype() == arg:
            return self.tokeniser.get_token()
        return None


def memoise(func):
    def memoise_wrapper(self, *args):
        pos = self.mark()
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, endpos = memo[key]
            self.reset(endpos)
        else:
            res = func(self, *args)
            endpos = self.mark()
            memo[key] = res, endpos
        return res
    return memoise_wrapper


def memoise_left_recursive(func):
    def memoise_left_rec_wrapper(self, *args):
        pos = self.mark()
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, endpos = memo[key]
            self.reset(endpos)
        else:
            memo[key] = lastres, lastpos = None, pos
            while True:
                self.reset(pos)
                res = func(self, *args)
                endpos = self.mark()
                if endpos <= lastpos:
                    break
                memo[key] = lastres, lastpos = res, endpos
            res = lastres
            self.reset(lastpos)
        return res
    return memoise_left_rec_wrapper


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
            return Node('atom', [atom])
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


if __name__ == '__main__':

    with open(sys.argv[1], 'r') as f:
        p = TestParser(Tokeniser(f.read()))
    print(p.let_stmt())
