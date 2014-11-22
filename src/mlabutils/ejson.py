#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.ejson module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import re

from mlabutils import BufferedIterator


class TextLoc(object):
    """Represents a location in text."""
    def __init__(self, offset, line, column):
        self.offset = offset
        self.line = line
        self.column = column

    def __repr__(self):
        return "TextLoc(%r, %r, %r)" % (
            self.offset,
            self.line,
            self.column
        )


class Token(object):
    def __init__(self, type, location, text, value):
        self.type = type
        self.location = location
        self.text = text
        self.value = value

    def __repr__(self):
        return "Token(%r, %r, %r, %r)" % (
            self.type,
            self.location,
            self.text,
            self.value,
        )

    def __str__(self):
        return self.text


class Lexer(object):
    """Extended JSON lexer.
    """

    def t_KEYWORD(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        lower = t.text.lower()
        if lower == "true":
            # t.type = "TRUE"
            t.value = True
        elif lower == "false":
            # t.type = "FALSE"
            t.value = False
        elif lower == "null":
            t.value = None
        return t

    def t_NUMBER(self, t):
        r"-?(0|[1-9][0-9]*)(\.[0-9]*)?([eE][-+]?[0-9]*)?"
        t.value = eval(t.text)
        return t

    def t_STRING(self, t):
        r"""\"(\\\"|[^\"\n])*\""""
        t.value = eval(t.text)
        return t

    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"

    t_COMMA = r"\,"
    t_SEMICOLON = r"\;"
    t_COLON = r"\:"
    t_EQUALS = r"\="

    def t_comment(self, t):
        r"(\/\/[^\n]*)|(\/\*.*?\*\/)"
        return None

    def t_ignore(self, t):
        r"\s+"
        self.line += t.value.count("\n")
        return None

    def __init__(self):
        self.token_specs = []
        self.ignore_token = None

        self._reflect()

    def _reflect(self):
        self.token_specs = []
        self.ignore_token = None

        for attr_name in dir(self):
            if not attr_name.startswith("t_"):
                continue

            token_name = attr_name[2:]
            attr_value = getattr(self, attr_name)

            if token_name == "ignore":
                self.ignore_token = self._reflect_token(token_name, attr_value)
                continue

            self.token_specs.append(self._reflect_token(token_name, attr_value))

    def _reflect_token(self, name, value):
        if isinstance(value, basestring):
            return (name, re.compile(value), lambda t: t)
        return (name, re.compile(value.__doc__), value)

    def scan(self, text, location = None):
        current_loc = location or TextLoc(0, 1, 1)

        self.offset = current_loc.offset
        self.line = current_loc.line
        self.column = current_loc.column

        while self.offset < len(text):
            if not self.ignore_token is None:
                token_spec, pattern, fn = self.ignore_token
                match = pattern.match(text, self.offset)
                if match is not None:
                    self.offset = match.end()
                    continue

            for token_type, pattern, fn in self.token_specs:
                match = pattern.match(text, self.offset)
                if match is not None:
                    start, end = match.span()
                    token = fn(Token(token_type, TextLoc(self.offset, self.line, self.column), match.group(0), match.group(0)))
                    if token is not None:
                        yield token
                    self.offset = end
                    break
            else:
                yield Token("UNKNOWN", TextLoc(self.offset, self.line, self.column), text[self.offset:], text[self.offset:])
                return

        while True:
            yield Token("EOF", TextLoc(self.offset, self.line, self.column), "", None)


class Parser(object):
    """Extended JSON parser.
    """

    def parse_string(self, text):
        lexer = Lexer()
        tokens = BufferedIterator(lexer.scan(text))
        success, value = self._parse_expression(tokens)
        return value

    def _parse_separator(self, tokens):
        while tokens.peek().type in ("COMMA", "SEMICOLON"):
            tokens.next()

    def _parse_expression(self, tokens):
        success, value = self._parse_list(tokens)
        if success:
            return True, value

        success, value = self._parse_dict(tokens)
        if success:
            return True, value

        success, value = self._parse_number(tokens)
        if success:
            return True, value

        success, value = self._parse_string(tokens)
        if success:
            return True, value

        return False, None

    def _parse_number(self, tokens):
        t = tokens.peek()
        if not t.type == "NUMBER":
            return False, None
        tokens.next()
        return True, t.value

    def _parse_string(self, tokens):
        t = tokens.peek()
        if t.type in ("STRING", "KEYWORD"):
            tokens.next()
            return True, t.value
        return False, None

    def _parse_list(self, tokens):
        # Parse left bracket
        if tokens.peek().type != "LBRACKET":
            return False, None
        tokens.next()

        # Parse list items
        values = []
        while True:
            success, result = self._parse_expression(tokens)
            if not success:
                break
            values.append(result)

            self._parse_separator(tokens)

        # Parse right bracket
        if tokens.peek().type != "RBRACKET":
            return True, values
        tokens.next()

        # Return result
        return True, values

    def _parse_dict(self, tokens):
        if tokens.peek().type != "LBRACE":
            return False, None
        tokens.next()

        elements = {}
        while True:
            token = tokens.peek()

            if not token.type in ("STRING", "KEYWORD"):
                break
            tokens.next()

            if tokens.peek().type in ("COLON", "EQUALS"):
                tokens.next()

            success, value = self._parse_expression(tokens)
            if not success:
                return False, value

            elements[token.value] = value

            self._parse_separator(tokens)

        if tokens.peek().type != "RBRACE":
            return True, elements
        tokens.next()

        return True, elements


def main():
    print __doc__


if __name__ == "__main__":
    main()

