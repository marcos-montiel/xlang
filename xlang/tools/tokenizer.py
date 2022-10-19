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
    keywords = {'const', 'var', 'and', 'or', 'not', 'if', 'elif', 'else',
                'for', 'in', 'while', 'func', 'try', 'except', 'class'}
    token_specification = [
        ('INTEGER', r'[0-9]+'),             # Integers
        ('FLOAT', r'[0-9]+\.[0-9]+')        # Floats
        ('IDENTIDIER', r'[A-Za-z_]+'),      # Identifiers
        ('LITERAL', r'(\".*\"|\'.*\'){1}'), # Literals
        ('PLUS_OP', r'\+'),                 # Addition operator
        ('MIN_OP', r'-'),                   # Subtraction operator
        ('MUL_OP', r'\*'),                  # Multiplication operator
        ('DIV_OP', r'/'),                   # Divition operator
        ('TIMES_OP', r'\*\*'),              # Exponentiation operator
        ('MOD_OP', r'%'),                   # Modulus operator
        ('ASS_OP', r'='),                   # Assignemt operator
        ('PLUS_ASS_OP',  r'\+='),           # Addition assignment operator
        ('MINUS_ASS_OP', r'-='),            # Subtration assignment operator
        ('EQ_OP', r'=='),                   # Equal operator
        ('GT_OP', r'>'),                    # Greater than operator
        ('LT_OP', r'<'),                    # Less than operator
        ('GT_EQ_OP', r'>='),                # Greater or equal operator
        ('LT_EQ_OP', r'<='),                # Less or equal operator
        ('NOT_EQ_OP', r'!='),               # Not equal operator
        ('COLON', r':'),                    # Colon
        ('L_PARENT', r'('),                 # Left Parenthesis
        ('R_PARENT', r')'),                 # Right Parenthesis
        ('TAB',      r'\t'),                # Tabulations
        ('NEWLINE',  r'\n'),                # Line endings
        ('COMMENT', r'(#\.*\n|/\*\.*\*/)'), # Comments
        ('SKIP',     r'[ ]+'),              # Skip over spaces
        ('MISMATCH', r'.'),                 # Any other character
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
        elif value in keywords:
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = specification.end()
            line_num += 1
            continue
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)
