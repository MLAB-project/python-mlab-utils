#!/usr/bin/python
# -*- coding: utf-8 -*-
"""tests.app_test module.

.. moduleauthor: Jan Milík <milikjan@fit.cvut.cz>
"""


import unittest

from mlabutils import app


class CLIAppBaseTest(unittest.TestCase):
    APP_NAME = "test_app"

    def test_constructor(self):
        test_app = app.CLIAppBase()

    def test_main(self):
        test_app = app.CLIAppBase(app_name = self.APP_NAME)
        test_app.main(arguments = [])
        self.assertIsNotNone(test_app.args)


class DaemonAppBase(CLIAppBaseTest):
    APP_NAME = "test_daemon"


def main():
    print(__doc__)


if __name__ == "__main__":
    main()

