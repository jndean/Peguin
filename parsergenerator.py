from pegparsing import BaseParser, memoise, memoise_left_recursive

import argparse
from bootstrapparsergenerator import (
    Grammar, Rule, Option, Repeat, Token, Optional,
    generate_parser_code
)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser('Generate a parser from a grammar file')
    argparser.add_argument('-i', '-g', '--grammar_file', required=True, help=(
        'The grammar file describing the parser(.peg extension)'))
    argparser.add_argument('-o', '--out_file', required=True, help=(
        'The python file to generate'))
    argparser.add_argument('-n', '-c', '--classname', default='Parser', help=(
        'The name of the generated parser class'))
    args = argparser.parse_args()

    code = generate_parser_code(args.grammar_file, args.classname)
    with open(args.out_file, 'w') as f:
        f.write(code)


class ParserGenerator(BaseParser):

    @memoise
    def rule_grammar(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_preamble()) is not None)
            and ((t1 := self.rule_rules()) is not None)
            and ((t2 := self.expect('ENDMARKER')) is not None)
        ):
            return Grammar(t1, t0)
        self.reset(pos)

        return None

    @memoise
    def rule_preamble(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('@')) is not None)
            and ((t1 := self.expect('CODEBLOCK')) is not None)
        ):
            return t1.string
        self.reset(pos)

        return None

    @memoise
    def rule_rules(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_rule()) is not None)
            and ((t1 := self.rule_rules()) is not None)
        ):
            return [t0] + t1
        self.reset(pos)

        if (True
            and ((t0 := self.rule_rule()) is not None)
        ):
            return [t0]
        self.reset(pos)

        return None

    @memoise
    def rule_rule(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('NONTERMINAL')) is not None)
            and ((t1 := self.expect(':')) is not None)
            and ((t2 := self.rule_options()) is not None)
            and ((t3 := self.expect(';')) is not None)
        ):
            return Rule(t0.string, t2)
        self.reset(pos)

        return None

    @memoise
    def rule_options(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_option()) is not None)
            and ((t1 := self.expect('|')) is not None)
            and ((t2 := self.rule_options()) is not None)
        ):
            return [t0] + t2
        self.reset(pos)

        if (True
            and ((t0 := self.rule_option()) is not None)
        ):
            return [t0]
        self.reset(pos)

        return None

    @memoise
    def rule_option(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_items()) is not None)
            and ((t1 := self.expect('CODEBLOCK')) is not None)
        ):
            return Option(t0, t1.string)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_items()) is not None)
        ):
            return Option(t0, None)
        self.reset(pos)

        return None

    @memoise
    def rule_items(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_item()) is not None)
            and ((t1 := self.rule_items()) is not None)
        ):
            return [t0] + t1
        self.reset(pos)

        if (True
            and ((t0 := self.rule_item()) is not None)
        ):
            return [t0]
        self.reset(pos)

        return None

    @memoise_left_recursive
    def rule_item(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_item()) is not None)
            and ((t1 := self.expect('*')) is not None)
        ):
            return Repeat(t0)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_item()) is not None)
            and ((t1 := self.expect('+')) is not None)
        ):
            return Repeat(t0, nonempty=True)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_item()) is not None)
            and ((t1 := self.expect('?')) is not None)
        ):
            return Optional(t0)
        self.reset(pos)

        if (True
            and ((t0 := self.expect('(')) is not None)
            and ((t1 := self.rule_options()) is not None)
            and ((t2 := self.expect(')')) is not None)
        ):
            return Rule(None, t1)
        self.reset(pos)

        if (True
            and ((t0 := self.rule_token()) is not None)
        ):
            return t0
        self.reset(pos)

        return None

    @memoise
    def rule_join(self):
        pos = self.mark()
        if (True
            and ((t0 := self.rule_item()) is not None)
            and ((t1 := self.expect('^')) is not None)
            and ((t2 := self.rule_item()) is not None)
        ):
            return Join(t0, t2)
        self.reset(pos)

        return None

    @memoise
    def rule_token(self):
        pos = self.mark()
        if (True
            and ((t0 := self.expect('TERMINAL')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('NONTERMINAL')) is not None)
        ):
            return t0
        self.reset(pos)

        if (True
            and ((t0 := self.expect('STRING')) is not None)
        ):
            return t0
        self.reset(pos)

        return None