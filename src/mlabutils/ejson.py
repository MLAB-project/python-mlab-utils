#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.ejson module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import re


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
    def __init__(self, type, text, value):
        self.type = type
        self.text = text
        self.value = value

    def __repr__(self):
        return "Token(%r, %r, %r)" % (
            self.type,
            self.text,
            self.value,
        )

    def __str__(self):
        return self.text


class Lexer(object):
    """Extended JSON lexer.
    """

    t_KEYWORD = r"[a-zA-Z_][a-zA-Z0-9_]*"

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
        current_loc = location or TexLoc(0, 1, 1)

        self.offset = current_loc.offset
        self.line = current_loc.line
        self.column = current_loc.column

        while self.offset < len(text):
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
                pass


class Parser(object):
    """Extended JSON parser.
    """

    def parse_string(self, text):
        pass


def main():
    print __doc__


if __name__ == "__main__":
    main()

