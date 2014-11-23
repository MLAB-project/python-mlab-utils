#!/usr/bin/python
# -*- coding: utf-8 -*-
"""tests.ejson_test module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import unittest

from mlabutils import config


class LoadFileTest(unittest.TestCase):
	def test_load_file(self):
		value = config.load_file("tests/radio-observer.json")
		self.assertIsNotNone(value)

