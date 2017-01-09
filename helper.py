#!/usr/bin/env python3

import os

__all__ = [
    "NotFoundHelper", "CGIHelper", "FoundFileHelper",
    "FoundDirIndexHelper", "FoundDirNoIndexHelper",
    "FailHelper", "ServerError"
]


class BaseHelper:
    """Parent for helpers."""

    @staticmethod
    def index_path(handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        raise NotImplementedError("Should implement this method")

    def do(self, handler):
        raise NotImplementedError("Should implement this method")


class NotFoundHelper(BaseHelper):
    """File or directory does not exist."""

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def do(self, handler):
        raise ServerError("%s not found" % handler.path)


class CGIHelper(BaseHelper):
    """Runnable python3."""

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def do(self, handler):
        handler.run_cgi(handler.full_path)


class FoundFileHelper(BaseHelper):
    """File exists."""

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def do(self, handler):
        handler.handle_file(handler.full_path)


class FoundDirIndexHelper(BaseHelper):
    """Serve index.html page for a directory."""

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def do(self, handler):
        handler.handle_file(self.index_path(handler))


class FoundDirNoIndexHelper(BaseHelper):
    """Serve listing for a directory without an index.html page."""

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def do(self, handler):
        handler.do_response(msg=handler.list_dir(handler.full_path).encode())


class FailHelper(BaseHelper):
    """If every case failed."""

    def test(self, handler):
        return True

    def do(self, handler):
        raise ServerError("Unknown %s" % handler.path)


class ServerError(Exception):
    """ Server error. """
    pass
