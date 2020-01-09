from pegparsing import BaseParser, memoise, memoise_left_recursive
from railwayparsergenerator import (
    Token, ThreadID, NumThreads, Lookup, Length, Uniop, Binop, ArrayLiteral,
    ArrayTensor, ArrayRange, Let, Unlet, Promote, Pop, Push, Swap, If
)

class RailwayParser(BaseParser):

    @memoise
    def rule_repetition0(self):
        result = []
        while (item := self.rule_statement()) is not None:
            result.append(item)
        if not result:
            return None
        return result

    @memoise
    def rule_program(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_repetition0()) is not None)
            and ((t1 := self.expect('ENDMARKER')) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_2(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_let_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_unlet_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_promote_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_swap_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_push_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_pop_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_if_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_statement(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_2()) is not None)
            and ((t1 := self.expect('NEWLINE')) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_repetition4(self):
        result = []
        while (item := self.rule_statement()) is not None:
            result.append(item)
        return result

    @memoise
    def rule_5(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('else')) is not None)
            and ((t1 := self.expect('NEWLINE')) is not None)
            and ((t2 := self.rule_repetition4()) is not None)
        ):
            return t2
        self.reset(pos)

        return None

    @memoise
    def rule_if_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('if')) is not None)
            and ((t1 := self.expect('(')) is not None)
            and ((t2 := self.rule_expression()) is not None)
            and ((t3 := self.expect(')')) is not None)
            and ((t4 := self.expect('NEWLINE')) is not None)
            and ((t5 := self.rule_repetition4()) is not None)
            and (((t6 := self.rule_5()) is not None) or True)
            and ((t7 := self.expect('fi')) is not None)
            and ((t8 := self.expect('(')) is not None)
            and (((t9 := self.rule_expression()) is not None) or True)
            and ((t10 := self.expect(')')) is not None)
        ):
            return If(t2, t5, t6, t9)
        self.reset(pos)

        return None

    @memoise
    def rule_pop_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('pop')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('=>')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Pop(t1, t3)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('pop')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('<=')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Pop(t3, t1)
        self.reset(pos)

        return None

    @memoise
    def rule_push_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('push')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('=>')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Push(t1, t3)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('push')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('<=')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Push(t3, t1)
        self.reset(pos)

        return None

    @memoise
    def rule_swap_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('swap')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('<=>')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Swap(t1, t3)
        self.reset(pos)

        return None

    @memoise
    def rule_promote_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('promote')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('=>')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Promote(t1, t3)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('promote')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
            and ((t2 := self.expect('<=')) is not None)
            and ((t3 := self.rule_lookup()) is not None)
        ):
            return Promote(t3, t1)
        self.reset(pos)

        return None

    @memoise
    def rule_11(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('=')) is not None)
            and ((t1 := self.rule_expression()) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_let_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('let')) is not None)
            and ((t1 := self.rule_name()) is not None)
            and (((t2 := self.rule_11()) is not None) or True)
        ):
            return Let(t1, t2)
        self.reset(pos)

        return None

    @memoise
    def rule_unlet_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('unlet')) is not None)
            and ((t1 := self.rule_name()) is not None)
            and (((t2 := self.rule_11()) is not None) or True)
        ):
            return Unlet(t1, t2)
        self.reset(pos)

        return None

    @memoise_left_recursive
    def rule_expression(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_expression()) is not None)
            and ((t1 := self.expect('+')) is not None)
            and ((t2 := self.rule_expr_()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expression()) is not None)
            and ((t1 := self.expect('-')) is not None)
            and ((t2 := self.rule_expr_()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expr_()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise_left_recursive
    def rule_expr_(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_expr_()) is not None)
            and ((t1 := self.expect('*')) is not None)
            and ((t2 := self.rule_expr__()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expr_()) is not None)
            and ((t1 := self.expect('/')) is not None)
            and ((t2 := self.rule_expr__()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expr_()) is not None)
            and ((t1 := self.expect('//')) is not None)
            and ((t2 := self.rule_expr__()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expr_()) is not None)
            and ((t1 := self.expect('%')) is not None)
            and ((t2 := self.rule_expr__()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expr__()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise_left_recursive
    def rule_expr__(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_expr__()) is not None)
            and ((t1 := self.expect('**')) is not None)
            and ((t2 := self.rule_atom()) is not None)
        ):
            return Binop(t0, t1, t2)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_atom()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_atom(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('(')) is not None)
            and ((t1 := self.rule_expression()) is not None)
            and ((t2 := self.expect(')')) is not None)
        ):
            return t1
        self.reset(pos)

        if (True
            and ((t0 := self.rule_array_literal()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_array_tensor()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_array_range()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_lookup()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('NUMBER')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_threadid()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_numthreads()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('-')) is not None)
            and ((t1 := self.rule_atom()) is not None)
        ):
            return Uniop(t0, t1)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('!')) is not None)
            and ((t1 := self.rule_atom()) is not None)
        ):
            return Uniop(t0, t1)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('#')) is not None)
            and ((t1 := self.rule_lookup()) is not None)
        ):
            return Length(t1)
        self.reset(pos)

        return None

    @memoise
    def rule_18(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect(',')) is not None)
            and ((t1 := self.rule_expression()) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_repetition19(self):
        result = []
        while (item := self.rule_18()) is not None:
            result.append(item)
        return result

    @memoise
    def rule_array_literal(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('[')) is not None)
            and ((t1 := self.expect(']')) is not None)
        ):
            return ArrayLiteral([])
        self.reset(pos)

        if (True
            and ((t0 := self.expect('[')) is not None)
            and ((t1 := self.rule_expression()) is not None)
            and ((t2 := self.rule_repetition19()) is not None)
            and ((t3 := self.expect(']')) is not None)
        ):
            return ArrayLiteral([t1] + t2)
        self.reset(pos)

        return None

    @memoise
    def rule_21(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('by')) is not None)
            and ((t1 := self.rule_expression()) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_array_range(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('[')) is not None)
            and ((t1 := self.rule_expression()) is not None)
            and ((t2 := self.expect('to')) is not None)
            and ((t3 := self.rule_expression()) is not None)
            and (((t4 := self.rule_21()) is not None) or True)
            and ((t5 := self.expect(']')) is not None)
        ):
            return ArrayRange(t1, t3, t4)
        self.reset(pos)

        return None

    @memoise
    def rule_array_tensor(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('[')) is not None)
            and ((t1 := self.rule_expression()) is not None)
            and ((t2 := self.expect('tensor')) is not None)
            and ((t3 := self.rule_expression()) is not None)
            and ((t4 := self.expect(']')) is not None)
        ):
            return ArrayTensor(t1, t3)
        self.reset(pos)

        return None

    @memoise
    def rule_24(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('[')) is not None)
            and ((t1 := self.rule_expression()) is not None)
            and ((t2 := self.expect(']')) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_repetition25(self):
        result = []
        while (item := self.rule_24()) is not None:
            result.append(item)
        return result

    @memoise
    def rule_lookup(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_name()) is not None)
            and ((t1 := self.rule_repetition25()) is not None)
        ):
            return Lookup(name=t0, index=tuple(t1))
        self.reset(pos)

        return None

    @memoise
    def rule_threadid(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('TID')) is not None)
        ):
            return ThreadID()
        self.reset(pos)

        return None

    @memoise
    def rule_numthreads(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('#TID')) is not None)
        ):
            return NumThreads()
        self.reset(pos)

        return None

    @memoise
    def rule_name(self):
        pos = self.mark()
        if (True
            and (((t0 := self.expect('.')) is not None) or True)
            and ((t1 := self.expect('NAME')) is not None)
        ):
            return ('.' if t0 is not None else '') + t1.string
        self.reset(pos)

        return None