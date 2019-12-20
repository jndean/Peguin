from types import ModuleType

from pegparsing import BaseParser, memoise, memoise_left_recursive, Token
from metatokeniser import tokenise


class Repeat:
    def __init__(self, contents, nonempty=False):
        self.contents = contents
        self.nonempty = nonempty

        self.first_set = set()
        if isinstance(contents, Token):
            self.first_set.add(contents.string)
        else:
            self.first_set = self.first_set.union(contents[0].first_set)

    def codegen(self, rules):
        subrule_name = f'subrule_{len(rules)}'
        rule_name = f'repeat_{subrule_name}'
        if isinstance(self.contents, Token):
            # A single token doesn't need its own rule, just an 'expect'
            snippet = f'self.expect({repr(self.contents.string)})'
        else:
            # Create a rule for the group that will be repeated
            subrule = Rule(subrule_name, self.contents)
            subrule.codegen(rules)
            snippet = f'self.rule_{subrule_name}()'

        # Create a rule that parses repetitions of the snippet
        lines = [f'    def {rule_name}(self):',
                 'result = []',
                 f'while (item := {snippet}) is not None:',
                 '    result.append(item)']
        if self.nonempty:
            lines += ['if not result:',
                      '    return None']
        lines.append('return result')
        rules.append('\n        '.join(lines))
        return rule_name


class Option:
    def __init__(self, items, action=None):
        self.items = items
        self.action = action

        self.first_set = set()
        if isinstance(items[0], Token):
            self.first_set.add(items[0].string)
        else:
            self.first_set = self.first_set.union(items[0].first_set)

    def __repr__(self):
        return f'Opt({self.items.__repr__()}, "{self.action}")'

    def codegen(self, rules):
        lines = ['if (True']
        for i, item in enumerate(self.items):
            if isinstance(item, Repeat):
                rule_name = item.codegen(rules)
                lines.append(
                    f'    and (t{i} := self.{rule_name})')
            elif item.type == 'TERMINAL' or item.type == 'STRING':
                lines.append(
                    f'    and (t{i} := self.expect({repr(item.string)}))')
            elif item.type == 'NONTERMINAL':
                lines.append(
                    f'    and (t{i} := self.rule_{item.string}())')

        lines.append(f'):')
        if self.action is not None:
            ret = self.action.strip().replace('\n', ' ')
        elif len(self.items) > 1:
            ret = f'[{", ".join([f"t{i}" for i in range(len(self.items))])}]'
        else:
            ret = 't0'
        lines.append(f'    return {ret}')
        return lines


class Rule:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    def __repr__(self):
        return f'Rule("{self.name}", {self.options.__repr__()})'

    def is_left_recursive(self):
        return any(self.name in opt.first_set for opt in self.options)

    def codegen(self, rules):
        lines = [f'    def rule_{self.name}(self):',
                 'pos = self.mark()']
        for option in self.options:
            lines += option.codegen(rules)
            lines.append('self.reset(pos)\n')
        lines.append('return None')
        decorator = ('    @memoise_left_recursive\n' if self.is_left_recursive()
                     else '    @memoise\n')
        rules.append(decorator + '\n        '.join(lines))


class Grammar:
    def __init__(self, rules, preamble=None):
        self.rules = rules
        self.preamble = '' if preamble is None else preamble

    def reduced_rules(self):
        existing = {}
        for rule in self.rules:
            if rule.name in existing:
                existing[rule.name].options += rule.options
            else:
                existing[rule.name] = rule
        return list(existing.values())

    def codegen(self, classname='GeneratedParser'):
        rules = []
        for r in self.reduced_rules():
            r.codegen(rules)
        return '\n\n'.join(
            ['from pegparsing import BaseParser, Token, memoise,'
             ' memoise_left_recursive',
             self.preamble,
             f'class {classname}(BaseParser):'] +
            rules)


class BootstrapMetaParser(BaseParser):


    @memoise
    def token(self):
        if ((t := self.expect('TERMINAL')) or
            (t := self.expect('NONTERMINAL')) or
            (t := self.expect('STRING'))
        ):
            return t
        return None

    @memoise
    def token_list(self):
        if token := self.token():
            if token_list := self.token_list():
                return [token] + token_list
            return [token]
        return None

    @memoise
    def option(self):
        if token_list := self.token_list():
            if action := self.expect('CODEBLOCK'):
                return Option(token_list, action.string)
            return Option(token_list, None)
        return None

    @memoise
    def options(self):
        if option := self.option():
            pos = self.mark()
            if self.expect('|'):
                if options := self.options():
                    return [option] + options
            self.reset(pos)
            return [option]
        return None

    @memoise
    def rule(self):
        pos = self.mark()
        if name := self.expect('NONTERMINAL'):
            if self.expect(':'):
                if options := self.options():
                    if self.expect(';'):
                        return Rule(name.string, options)
        self.reset(pos)
        return None

    @memoise
    def rule_list(self):
        if rule := self.rule():
            if rule_list := self.rule_list():
                return [rule] + rule_list
            return [rule]
        return None

    @memoise
    def preamble(self):
        pos = self.mark()
        if self.expect('@') and (code := self.expect('CODEBLOCK')):
            return code.string
        self.reset(pos)
        return None

    @memoise
    def preambles(self):
        pos = self.mark()
        if preamble := self.preamble():
            if preambles := self.preambles():
                return preamble + '\n' + preambles
            return preamble
        self.reset(pos)
        return None

    def rule_grammar(self):
        pos = self.mark()
        preambles = self.preambles()
        if (rule_list := self.rule_list()) and self.expect('ENDMARKER'):
            return Grammar(rule_list, preambles)
        self.reset(pos)
        return None


if __name__ == '__main__':

    def generate_parser(metaparser_class, grammar_path, parser_name='Parser'):
        """
        Use the metaparser_class to parse a grammar file and generate a parser.
        """
        with open(grammar_path, 'r') as f:
            tokens = tokenise(f.read())
        # Initialise a metaparser of the given class to parse the grammar tokens
        metaparser = metaparser_class(tokens)
        # Parse the tokens to produce a grammar object
        grammar = metaparser.rule_grammar()
        # Generate parser code from the grammar
        code = grammar.codegen(parser_name)
        open('tmp.py', 'w').write(code)
        # Load the code into a fake module to compile to python bytecode
        module = ModuleType('syntheticmodule')
        exec(code, module.__dict__)
        # Get the parser
        parser = getattr(module, parser_name)
        return parser, code


    # Use the simple boostrap parser to parse the basic initial grammar
    MetaParser0, MetaParser0_code = generate_parser(
        metaparser_class=BootstrapMetaParser,
        grammar_path='Grammars/metagrammar0.peg',
    )

    # Can the generated metaparser parse its own grammar
    # and hence generate itsef stably?
    MetaParser00, MetaParser00_code = generate_parser(
        metaparser_class=MetaParser0,
        grammar_path='Grammars/metagrammar0.peg',
    )
    assert(MetaParser0_code == MetaParser00_code)

    # Add the repetition feature
    MetaParser1, MetaParser1_code = generate_parser(
        metaparser_class=MetaParser0,
        grammar_path='Grammars/metagrammar1.peg',
    )

    # Make use of the repetitions feature to simplify the grammar
    MetaParser2, MetaParser2_code = generate_parser(
        metaparser_class=MetaParser1,
        grammar_path='Grammars/metagrammar2.peg',
    )
    print(MetaParser2_code)

    print(MetaParser2)
