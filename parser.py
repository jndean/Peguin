#!/usr/bin/env python3

from collections import namedtuple
import sys

from newlexer import lex
from metatokeniser import lex as metalex


Node = namedtuple("Node", ["type", "children"])

"""
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
"""


class Parser:
    def __init__(self, token_generator):
        self.gen = token_generator
        self.tokens = []
        self.token_pos = 0
        self.memos = {}

    def mark(self):
        return self.token_pos

    def reset(self, pos):
        self.token_pos = pos

    def peek_token(self):
        if self.token_pos == len(self.tokens):
            try:
                self.tokens.append(next(self.gen))
            except StopIteration:
                self.tokens.append(None)
        return self.tokens[self.token_pos]

    def get_token(self):
        token = self.peek_token()
        self.token_pos += 1
        return token

    def expect(self, arg):
        token = self.peek_token()
        if token and token.gettokentype() == arg:
            return self.get_token()
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


class MetaParser(Parser):

    @memoise
    def token(self):
        terminal = self.expect('TERMINAL')
        if terminal:
            return terminal
        nonterminal = self.expect('NONTERMINAL')
        if nonterminal:
            return nonterminal
        return None

    @memoise
    def token_list(self):
        token = self.token()
        if token:
            token_list = self.token_list()
            if token_list:
                return Node('token_list', [token] + token_list.children)
            return Node('token_list', [token])
        return None

    @memoise
    def options(self):
        token_list = self.token_list()
        if token_list:
            pos = self.mark()
            op = self.expect('OR')
            if op:
                options = self.options()
                if options:
                    return Node('options', [token_list] + options.children)
            self.reset(pos)
            return Node('options', [token_list])
        return None

    @memoise
    def rule(self):
        pos = self.mark()

        name = self.expect('NONTERMINAL')
        if name is None:
            return None

        if self.expect('COLON') is None:
            self.reset(pos)
            return None

        options = self.options()
        if options is None:
            self.reset(pos)
            return None


        return Node('rule', [name, options])


class RuleGenerator:
    def __init__(self, parser_type, lex_method):
        self.parser_type = parser_type
        self.lex_method = lex_method

    def rule(self, rule_str):
        rule_tree = self.parser_type(self.lex_method(rule_str)).rule()
        name, *rule_parts = rule_tree.children
        def ret(func):
            print(f'wrapping wrapped with {rule_str}')
            return func
        return ret


rules = """
rule : NONTERMINAL COLON options SEMI ;
options : token_list OR options | token_list ;
token_list : token token_list | token ;
token : TERMINAL | NONTERMINAL ;
"""

rules = """
"""


r = RuleGenerator(MetaParser, metalex)


@r.rule("x : b c")
def myfunc(p):
    print(f"In myfunc, p = {p}")
    

myfunc([3, 4, 5])
    

if __name__ == '__main__':

    """
    for line in rules.strip().splitlines():
        name, colon, *args = line.split()
        if colon != ':' or not args:
            raise ValueError('Badly formatted rule:', line)

        outstr = ''

        if name == args[0]:
            outstr += '    @memoise_left_recursive\n'
        else:
            outstr += '    @memoise\n'

        outstr += f'    def {name}(self):'
        indentation = 2
    """

    p = MetaParser(metalex(rules))
    print(p.rule())
    quit()
    
    with open(sys.argv[1], 'r') as f:
        p = TestParser(lex(f.read()))
    print(p.let_stmt())
