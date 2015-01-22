#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.app module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import os
from os import path
import sys
import argparse
import logging

import lockfile
import daemon

from mlabutils import config
from mlabutils.utils import getClassLogger


class CLIAppBase(object):
    """Base class for comman-line applications.
    """

    def __init__(self, app_name = None):
        self.app_name = app_name
        if self.app_name is None:
            self.app_name = self._get_app_name()

        self.arg_parser = argparse.ArgumentParser()
        self.args = None

        self.read_user_config = True
        self.read_system_config = True
        self.config = None

        self.logger = getClassLogger(self)

        self.uncaught_exception_exit_code = 1

    def _get_app_name(self):
        try:
            app_name = path.basename(sys.argv[0]).split(".")[0]
        except Exception:
            app_name = "app"
        return app_name

    def setup_app(self):
        pass

    def setup_args(self):
        """Override to setup custom comman-line arguments.
        """
        self.arg_parser.add_argument(
            "-c", "--config",
            metavar = "CONFIG_FILE",
            dest = "config_file",
            help = "configuration file",
            default = None)

    def parse_args(self, arguments = None):
        self.setup_args()
        self.args = self.arg_parser.parse_args(arguments)

    def get_config_file(self, log = False):
        if log:
            log_fn = lambda f, *a: sys.stderr.write((f + "\n") % a)
        else:
            log_fn = lambda *a, **kw: None

        if self.args.config_file is not None:
            file_name = self.args.config_file
            if path.isfile(file_name):
                log_fn("Found config file %s.", file_name)
                return file_name
            else:
                log_fn("Config file %s doesn't exist.", file_name)

        if self.read_user_config:
            file_name = path.join(
                os.getenv("HOME"), "." + self.app_name + ".conf")
            if path.isfile(file_name):
                log_fn("Found config file %s.", file_name)
                return file_name
            else:
                log_fn("Config file %s doesn't exist.", file_name)

        if self.read_system_config:
            file_name = path.join("/etc", self.app_name)
            if path.isfile(file_name):
                log_fn("Found config file %s.", file_name)
                return file_name
            else:
                log_fn("Config file %s doesn't exist.", file_name)

        return None

    def read_config(self):
        file_name = self.get_config_file(True)
        if file_name is None:
            sys.stderr.write("No config file found.\n")
            self.logger.warn("No config file found.")
            self.config = {}
            return False

        self.logger.info("Reading config file %s...", file_name)
        self.config = config.load_file(file_name)
        return True
    
    def setup_logging(self):
        logging.root.handlers = []
        logging.basicConfig(
            level = logging.INFO,
            filename = self.get_default_log_filename(),
            format = "%(asctime)s   %(process)s  %(name)s  %(levelname)s  %(message)s")
    
    def get_default_log_filename(self):
        #return path.abspath(path.join(os.getenv("HOME"), self.app_name + ".log"))
        return "/var/log/%s.log" % (self.app_name, )
    
    def run(self):
        """Override to implement the application's main method.
        """
        pass

    def main(self, arguments = None):
        self.setup_app()
        self.parse_args(arguments)
        self.read_config()
        self.setup_logging()
        try:
            exit_code = self.run()
        except Exception as e:
            self.logger.exception("Unexpected error occured in application.")
            self.exit(self.uncaught_exception_exit_code)
        if isinstance(exit_code, int):
            self.exit(exit_code)

    def exit(self, exit_code = 0):
        self.logger.info("Exiting with code %d." % (exit_code, ))
        sys.exit(exit_code)


class DaemonAppBase(CLIAppBase):
    def setup_app(self):
        self.daemon_context = daemon.DaemonContext(
            pidfile = lockfile.FileLock(self.pid_file_name),
        )

        self.pidfile_locked_exit_code = 2

    @property
    def pid_file_name(self):
        return "/var/run/%s.pid" % (self.app_name, )

    def run(self):
        if self.daemon_context.pidfile.is_locked():
            sys.stderr.write("PID file %s is locked. Daemon %s is probably running.\n" % (
                self.pid_file_name,
                self.app_name,
            ))
            return self.pidfile_locked_exit_code

        self.logger.info("Starting daemon...")
        with self.daemon_context:
            self.setup_logging()
            self.logger.info("Daemon started with PID %d.", os.getpid())
            try:
                self.run_daemon()
            except Exception as e:
                self.logger.exception("Uncaught exception occured in daemon. Daemon will exit.")
                return self.uncaught_exception_exit_code

        self.logger.info("Daemon started.")

    def run_daemon(self):
        pass


def main():
    print __doc__


if __name__ == "__main__":
    main()

