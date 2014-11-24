#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.app module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import os
from os import path
import sys
import argparse

from mlabutils import config


class CLIAppBase(object):
    """Base class for comman-line applications.
    """
    
    def __init__(self, app_name = None):
        self.app_name = app_name
        if self.app_name is None:
            try:
                self.app_name = path.basename(sys.argv[0]).split(".")[0]
            except Exception:
                self.app_name = "app"
        
        self.arg_parser = argparse.ArgumentParser()
        self.args = None

        self.config = None
    
    def setup_app(self):
        pass
    
    def setup_args(self):
        """Override to setup custom comman-line arguments.
        """
        pass
    
    def parse_args(self, arguments = None):
        self.setup_args()
        self.args = self.arg_parser.parse_args(arguments)
    
    def get_config_file(self):
        file_name = path.join(os.getenv("HOME"), "." + self.app_name)
        print file_name
        if path.isfile(file_name):
            return file_name
        return None
    
    def read_config(self):
        file_name = self.get_config_file()
        if file_name is None:
            return

        self.config = config.load_file(file_name)
    
    def run(self):
        """Override to implement the application's main method.
        """
        pass
    
    def main(self, arguments = None):
        self.setup_app()
        self.parse_args(arguments)
        self.read_config()
        exit_code = self.run()
        if isinstance(exit_code, int):
            sys.exit(exit_code)


def main():
    print __doc__


if __name__ == "__main__":
    main()

