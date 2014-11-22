#!/usr/bin/python
# -*- coding: utf-8 -*-
"""tests.ejson_test module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import unittest

from mlabutils import ejson


class LexerTest(unittest.TestCase):
    def test_boolean_keywords(self):
        lexer = ejson.Lexer()

        tokens = lexer.scan("true")

        token = tokens.next()
        self.assertEquals("KEYWORD", token.type)
        self.assertEquals("true", token.text)
        self.assertEquals(True, token.value)

    def test_number(self):
        lexer = ejson.Lexer()

        tokens = lexer.scan("0")

        token = tokens.next()
        self.assertEquals("NUMBER", token.type)
        self.assertEquals("0", token.text)
        self.assertEquals(0, token.value)


class ParserTest(unittest.TestCase):
    def test_constructor(self):
        parser = ejson.Parser()

    def test_parse_boolean(self):
        parser = ejson.Parser()

        value = parser.parse_string("null")
        self.assertEquals(None, value)

        value = parser.parse_string("NULL")
        self.assertEquals(None, value)

        value = parser.parse_string("Null")
        self.assertEquals(None, value)

    def test_parse_boolean(self):
        parser = ejson.Parser()

        value = parser.parse_string("true")
        self.assertEquals(True, value)

        value = parser.parse_string("false")
        self.assertEquals(False, value)

    def test_parse_number(self):
        parser = ejson.Parser()

        value = parser.parse_string("0")
        self.assertEquals(0, value)

        value = parser.parse_string("123")
        self.assertEquals(123, value)

    def test_parse_string(self):
        parser = ejson.Parser()

        value = parser.parse_string("\"\"")
        self.assertEquals("", value)

        value = parser.parse_string("\"abc\"")
        self.assertEquals("abc", value)

        value = parser.parse_string("\"\\\"\"")
        self.assertEquals("\"", value)

    def test_parse_comment(self):
        parser = ejson.Parser()

        value = parser.parse_string("// some comment\ntrue")
        self.assertEquals(True, value)

        value = parser.parse_string("/* some comment */true")
        self.assertEquals(True, value)

    def test_parse_file(self):
        parser = ejson.Parser()

        value = parser.parse_file("tests/radio-observer.json")
        import pprint
        pprint.pprint(value)
        self.assertIsInstance(value, dict)

        self.assertEquals("system:capture_1", value["jack_left_port"])

