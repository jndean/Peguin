from metatokeniser import tokenise
from pegparsing import BaseParser, memoise


class Token:
    __slots__ = ['type', 'string', 'line', 'col', 'first_set']

    def __init__(self, type, string, line, col):
        self.type = type
        self.string = string
        self.line = line
        self.col = col
        self.first_set = {string}

    def __str__(self):
        return repr(self.string)

    def __repr__(self):
        return f'Token({repr(self.type)}, {repr(self.string)})'

    def codegen(self, rules):
        if self.type == 'TERMINAL' or self.type == 'STRING':
            return f'self.expect({repr(self.string)})'
        if self.type == 'NONTERMINAL':
            return f'self.rule_{self.string}()'
        raise ValueError(
            f"Don't know how to generate code for a token of type {self.type}")


class Optional:
    def __init__(self, content):
        self.content = content
        self.first_set = content.first_set

    def codegen(self, rules):
        return self.content.codegen(rules)


class Repeat:
    def __init__(self, content, nonempty=False):
        self.content = content
        self.nonempty = nonempty
        self.first_set = content.first_set

    def codegen(self, rules):
        snippet = self.content.codegen(rules)
        rule_name = f'rule_repetition{len(rules)}'
        func_head = (f'    @memoise\n'
                     f'    def {rule_name}(self):\n')
        func_call = f'self.{rule_name}()'

        lines = ['result = []',
                 f'while (item := {snippet}) is not None:',
                 '    result.append(item)']
        if self.nonempty:
            lines += ['if not result:',
                      '    return None']
        lines.append('return result')
        func_body = '\n'.join('        ' + l for l in lines)

        if func_body in rules:
            func_head, func_call = rules[func_body]
        else:
            rules[func_body] = func_head, func_call

        return func_call


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
            snippet = item.codegen(rules)
            if isinstance(item, (Token, Repeat, Rule)):
                lines.append(
                    f'    and ((t{i} := {snippet}) is not None)')
            elif isinstance(item, Optional):
                lines.append(
                    f'    and (((t{i} := {snippet}) is not None) or True)')
            elif isinstance(item, Token):
                lines.append(
                    f'    and ((t{i} := {snippet}) is not None)')
            else:
                raise ValueError(type(item), item)
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
        self.first_set = set()
        for option in options:
            self.first_set = self.first_set.union(option.first_set)

    def __repr__(self):
        return f'Rule("{self.name}", {self.options.__repr__()})'

    def is_left_recursive(self):
        return (self.name is not None and
                any(self.name in opt.first_set for opt in self.options))

    def codegen(self, rules):
        lines = ['pos = self.mark()']
        for option in self.options:
            lines += option.codegen(rules)
            lines.append('self.reset(pos)\n')
        lines.append('return None')
        func_body = '\n'.join('        ' + l for l in lines)

        func_name = f'rule_{len(rules) if self.name is None else self.name}'
        decorator = ('memoise_left_recursive' if self.is_left_recursive()
                     else 'memoise')
        func_head = (f'    @{decorator}\n'
                     f'    def {func_name}(self):\n')
        func_call = f'self.{func_name}()'

        if func_body in rules:
            func_head, func_call = rules[func_body]
        else:
            rules[func_body] = func_head, func_call

        return func_call


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
        rules = {}
        for rule in self.rules:
            rule.codegen(rules)
        code = ('from pegparsing import BaseParser, memoise, '
                'memoise_left_recursive\n'
                f'{self.preamble}\n\n'                
                f'class {classname}(BaseParser):\n\n'
                + '\n\n'.join(head + body for body, (head, _) in rules.items()))
        return code


class MetaParser(BaseParser):

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
            if tokens := self.token_list():
                return [token] + tokens
            return [token]
        return None

    @memoise
    def option(self):
        if tokens := self.token_list():
            if action := self.expect('CODEBLOCK'):
                return Option(tokens, action.string)
            return Option(tokens, None)
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
        if ((name := self.expect('NONTERMINAL'))
                and (self.expect(':'))
                and (options := self.options())
                and (self.expect(';'))):
            return Rule(name.string, options)
        self.reset(pos)
        return None

    @memoise
    def rules(self):
        if rule := self.rule():
            if rules := self.rules():
                return [rule] + rules
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

    def grammar(self):
        pos = self.mark()
        preambles = self.preambles()
        if (rules := self.rules()) and self.expect('ENDMARKER'):
            return Grammar(rules, preambles)
        self.reset(pos)
        return None


# -------------------- Code to run the metaparser ------------------------- #

def generate_parser_code(grammar_file, classname='Parser'):
    with open(grammar_file, 'r') as f:
        tokens = tokenise(f.read(), TokenClass=Token)
    metaparser = MetaParser(tokens)
    grammar = metaparser.grammar()
    code = grammar.codegen(classname)
    return code


if __name__ == '__main__':
    code = generate_parser_code('Grammars/metagrammar.peg', 'ParserGenerator')
    with open('parsergenerator.py', 'w') as f:
        f.write(code)
