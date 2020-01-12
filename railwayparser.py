from pegparsing import BaseParser, memoise, memoise_left_recursive
from railwayparsergenerator import (
    Token, ThreadID, NumThreads, Lookup, Length, Uniop, Binop, ArrayLiteral,
    ArrayTensor, ArrayRange, Let, Unlet, Promote, Pop, Push, Swap, If, Loop,
    For, Modop, Barrier, Mutex, Modop, Print, PrintLn, DoUndo
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

        if (True
            and ((t0 := self.rule_loop_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_for_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_modify_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_barrier_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_mutex_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_print_stmt()) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_doundo_stmt()) is not None)
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
            and ((t0 := self.expect('yield')) is not None)
            and ((t1 := self.expect('NEWLINE')) is not None)
            and ((t2 := self.rule_repetition4()) is not None)
        ):
            return t2
        self.reset(pos)

        return None

    @memoise
    def rule_doundo_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('do')) is not None)
            and ((t1 := self.expect('NEWLINE')) is not None)
            and ((t2 := self.rule_repetition4()) is not None)
            and (((t3 := self.rule_5()) is not None) or True)
            and ((t4 := self.expect('undo')) is not None)
        ):
            return DoUndo(t2, t3)
        self.reset(pos)

        return None

    @memoise
    def rule_print_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('print')) is not None)
            and ((t1 := self.expect('(')) is not None)
            and ((t2 := self.rule_printables()) is not None)
            and ((t3 := self.expect(')')) is not None)
        ):
            return Print(t2)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('println')) is not None)
            and ((t1 := self.expect('(')) is not None)
            and ((t2 := self.rule_printables()) is not None)
            and ((t3 := self.expect(')')) is not None)
        ):
            return PrintLn(t2)
        self.reset(pos)

        return None

    @memoise
    def rule_8(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('STRING')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.rule_expression()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_9(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect(',')) is not None)
            and ((t1 := self.rule_8()) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_repetition10(self):
        result = []
        while (item := self.rule_9()) is not None:
            result.append(item)
        return result

    @memoise
    def rule_printables(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_8()) is not None)
            and ((t1 := self.rule_repetition10()) is not None)
        ):
            return [t0] + t1
        self.reset(pos)

        return None

    @memoise
    def rule_barrier_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('barrier')) is not None)
            and ((t1 := self.expect('STRING')) is not None)
        ):
            return Barrier(t1.string)
        self.reset(pos)

        return None

    @memoise
    def rule_mutex_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('mutex')) is not None)
            and ((t1 := self.expect('STRING')) is not None)
            and ((t2 := self.expect('NEWLINE')) is not None)
            and ((t3 := self.rule_repetition4()) is not None)
            and ((t4 := self.expect('xetum')) is not None)
        ):
            return Mutex(t1.string, t3)
        self.reset(pos)

        return None

    @memoise
    def rule_modify_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_lookup()) is not None)
            and ((t1 := self.rule_modop_symbol()) is not None)
            and ((t2 := self.rule_expression()) is not None)
        ):
            return Modop(t0, t1, t2)
        self.reset(pos)

        return None

    @memoise
    def rule_for_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('for')) is not None)
            and ((t1 := self.expect('(')) is not None)
            and ((t2 := self.rule_expression()) is not None)
            and ((t3 := self.expect('in')) is not None)
            and ((t4 := self.rule_expression()) is not None)
            and ((t5 := self.expect(')')) is not None)
            and ((t6 := self.expect('NEWLINE')) is not None)
            and ((t7 := self.rule_repetition4()) is not None)
            and ((t8 := self.expect('rof')) is not None)
        ):
            return For(t2, t4, t7)
        self.reset(pos)

        return None

    @memoise
    def rule_loop_stmt(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('loop')) is not None)
            and ((t1 := self.expect('(')) is not None)
            and ((t2 := self.rule_expression()) is not None)
            and ((t3 := self.expect(')')) is not None)
            and ((t4 := self.expect('NEWLINE')) is not None)
            and ((t5 := self.rule_repetition4()) is not None)
            and ((t6 := self.expect('pool')) is not None)
            and ((t7 := self.expect('(')) is not None)
            and (((t8 := self.rule_expression()) is not None) or True)
            and ((t9 := self.expect(')')) is not None)
        ):
            return Loop(t2, t5, t8)
        self.reset(pos)

        return None

    @memoise
    def rule_17(self):
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
            and (((t6 := self.rule_17()) is not None) or True)
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
    def rule_23(self):
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
            and (((t2 := self.rule_23()) is not None) or True)
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
            and (((t2 := self.rule_23()) is not None) or True)
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
    def rule_30(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect(',')) is not None)
            and ((t1 := self.rule_expression()) is not None)
        ):
            return t1
        self.reset(pos)

        return None

    @memoise
    def rule_repetition31(self):
        result = []
        while (item := self.rule_30()) is not None:
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
            and ((t2 := self.rule_repetition31()) is not None)
            and ((t3 := self.expect(']')) is not None)
        ):
            return ArrayLiteral([t1] + t2)
        self.reset(pos)

        return None

    @memoise
    def rule_33(self):
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
            and (((t4 := self.rule_33()) is not None) or True)
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
    def rule_36(self):
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
    def rule_repetition37(self):
        result = []
        while (item := self.rule_36()) is not None:
            result.append(item)
        return result

    @memoise
    def rule_lookup(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_name()) is not None)
            and ((t1 := self.rule_repetition37()) is not None)
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

    @memoise
    def rule_modop_symbol(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('+=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('-=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('*=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('/=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('//=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('**=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('%=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('^=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('|=')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('&=')) is not None)
        ):
            return t0
        self.reset(pos)

        return None