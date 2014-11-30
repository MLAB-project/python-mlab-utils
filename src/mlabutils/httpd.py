#!/usr/bin/python
# -*- coding: utf-8 -*-
"""mlabutils.httpd module.

.. moduleauthor:: Jan Milík <milikjan@fit.cvut.cz>
"""


import SimpleHTTPServer
import SocketServer

from mlabutils.utils import getClassLogger


class HTTPHandlerBase(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        method = self._route()

        try:
            method()
        except Exception as e:
            self.server.exception(
                "Exception occured while handling POST request.")

    def do_POST(self):
        method = self._route()

        self.form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        try:
            method()
        except Exception as e:
            self.server.exception(
                "Exception occured while handling GET request.")

    def _route(self):
        self.parsed_url = urlparse.urlparse(self.path)

        path = self.parsed_url.path
        if not path.startswith("/"):
            path = "/" + path

        method = self.route(path) or self._handle_unknown
        return method

    def route(self, path):
        return None

    def handle_unknown(self):
        self.send_response(404, """
            <html>
                <body>
                    <h1>Error 404 - Page Not Found</h1>
                    <p>%s</p>
                </body>
            </html>
        """ % (self.parsed_url.path, ))


class HTTPServerBase(SocketServer.TCPServer):
    DEFAULT_HANDLER_CLASS = HTTPHandlerBase

    def __init__(self,
                 server_address,
                 handler_class = None,
                 bind_and_activate = True,
                 logger = None):
        SocketServer.TCPServer.__init__(
            self,
            server_address,
            handler_class or self.DEFAULT_HANDLER_CLASS,
            bind_and_activate
        )

        if logger is None:
            self.logger = getClassLogger(self)
        else:
            self.logger = logger

        self.init_server()

    def init_server(self):
        pass

    def log_error(self, format, *args):
        self.logger.error(format, *args)

    def log_message(self, format, *args):
        self.logger.info(format, *args)


def main():
    print __doc__


if __name__ == "__main__":
    main()

