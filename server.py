#!/usr/bin/env python3

import os
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler, HTTPStatus

from helper import *


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    """Customized simple HTTP request handler to serve GET request."""

    error_message_format = """\
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h2>Error response</h2>
            <p>Error code: {code}</p>
            <p>Message: {msg}</p>
        </body>
    </html>
    """

    listing_directory_format = """\
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Directory list</title>
        </head>
        <body>
            <h2>Directory list</h2>
            <ul>
                {}
            </ul>
        </body>
    </html>
    """

    def do_GET(self):
        """Serve a GET request."""

        # use parent method to convert relative path to system path
        self.full_path = self.translate_path(self.path)
        # chain of helpers in order. Can easily add more
        helpers = [NotFoundHelper(),
                   CGIHelper(),
                   FoundFileHelper(),
                   FoundDirIndexHelper(),
                   FoundDirNoIndexHelper(),
                   FailHelper()]
        try:
            for helper in helpers:
                if helper.test(self):
                    helper.do(self)
                    break
        except Exception as e:
            self.handle_error(msg=str(e))

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                msg = reader.read()
            self.do_response(msg=msg)
        except IOError as e:
            msg = "%s cannot be read: %s" % (self.path, e)
            self.handle_error(msg=msg)

    def list_dir(self, full_path):
        """Return listing page for the directory."""
        try:
            entries = os.listdir(full_path)
            bullets = ["<li>{}</li>".format(e) for e in entries if not e.startswith('.')]
            return self.listing_directory_format.format('\n'.join(bullets))
        except OSError as e:
            msg = "{0} cannot be listed: {1}".format(self.path, e)
            self.handle_error(msg=msg)
            return None

    def run_cgi(self, full_path):
        """Simple way to run python3 CGI script."""
        cmd = ["python3", full_path]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        self.do_response(msg=stdout)

    def do_response(self, code=HTTPStatus.OK, msg=None):
        """Send response to client."""
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def handle_error(self, code=HTTPStatus.NOT_FOUND, msg=None):
        msg = self.error_message_format.format(code=code, msg=msg)
        self.do_response(code, msg.encode())


if __name__ == '__main__':
    server_address = ('', 8080)
    # replace with SimpleHTTPRequestHandler to see parent handler
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()
