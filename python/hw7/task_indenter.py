"""Indenter decorator"""
from contextlib import ContextDecorator
from functools import wraps

class Indenter(ContextDecorator):
    """Decorator Indenter"""
    def __init__(self, indent_str=" "*4, indent_level=0):
        self.indent_str = indent_str
        self.indent_level = indent_level

    def __enter__(self):
        self.indent_level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.indent_level -= 1

    def print(self, text):
        print(self.indent_str * (self.indent_level - 1) + text)
