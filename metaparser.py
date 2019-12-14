
from pegparsing import BaseParser, memoise, memoise_left_recursive
from metatokeniser import lex as metalex


class Option:
    def __init__(self, items, action=None):
        self.items = items
        self.action = action

    def __repr__(self):
        return f'Opt({self.items.__repr__()}, "{self.action}")'

    def codegen(self):
        lines = ['if (True and']
        for i, item in enumerate(self.items):
            if item.type == 'TERMINAL':
                lines.append(
                    f'    and (t{i} := self.expect({repr(item.string)}))')
            elif item.type == 'NONTERMINAL':
                rule_name = f'__rule_{item.string}'
                lines.append(
                    f'    and (t{i} := self.{rule_name}())')
        lines.append(f'):')
        if self.action is not None:
            ret = self.action
        else:
            ret = f'[{", ".join([f"t{i}" for i in range(len(self.items))])}]'
        lines.append(f'    return {ret}')
        return lines


class Rule:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    def __repr__(self):
        return f'Rule("{self.name}", {self.options.__repr__()})'

    def codegen(self):
        lines = ['pos = self.mark()']
        for option in self.options:
            lines += option.codegen()
            lines.append('self.reset(pos)')
            lines.append('')
        lines.append('return None')
        return lines


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
            if token_list := self.token_list():
                return [token] + token_list
            return [token]
        return None

    @memoise
    def option(self):
        if token_list := self.token_list():
            if action := self.expect('ACTION'):
                action_str = action.string[1:-1].replace('\n', ' ')
                return Option(token_list, action_str)
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

    def start(self):
        pos = self.mark()
        if rule_list := self.rule_list():
            if self.expect('ENDMARKER'):
                return rule_list
        self.reset(pos)
        return None


if __name__ == '__main__':

    p = MetaParser(metalex("""
        start : rule_list ENDMARKER ;
        rule_list : rule rule_list | rule ;
        rule : NONTERMINAL ':' options ';' ;
        options : option '|' options | option ;
        option : token_list ACTION | token_list ;
        token_list : token token_list | token ;
        token : TERMINAL {t0.string} | NONTERMINAL {t0.string} | STRING ;
    """))

    for r in p.start():
        print(r)

    print("\n\n\n")
    p = MetaParser(metalex('token_list : token token_list | token ;'))
    rule = p.rule()
    print(rule)
    print('\n'.join(rule.codegen()))