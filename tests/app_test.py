#!/usr/bin/python
# -*- coding: utf-8 -*-
"""app_test module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import unittest

from mlabutils import app


class CLIAppBaseTest(unittest.TestCase):
    def test_constructor(self):
        test_app = app.CLIAppBase()
    
    def test_main(self):
        test_app = app.CLIAppBase(app_name = "test_app")
        test_app.main(arguments = [])
        self.assertIsNotNone(test_app.args)


def main():
    print __doc__


if __name__ == "__main__":
    main()

