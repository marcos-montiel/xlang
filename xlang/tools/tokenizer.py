"""
This module generate tokens
"""

import re


class Token:
    """
    This class create the properties of the tokens object
    """

    def __init__(self, kind, value, line, column):
        self.type = kind
        self.value = value
        self.line = line
        self.column = column


def tokenize(file):
    """
    This function scan a file and return a token
    """
    keywords = {'if', 'for', 'while', 'int', 'return', 'str'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r'='),            # Assignment operator
        ('ID',       r'[A-Za-z]+'),    # Identifiers
        ('ARITH_OP', r'[+\-*/]'),      # Arithmetic operators
        ('TAB',      r'\t'),           # Tabulations
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ ]+'),         # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for specification in re.finditer(tok_regex, file):
        kind = specification.lastgroup
        value = specification.group()
        column = specification.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = specification.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)
