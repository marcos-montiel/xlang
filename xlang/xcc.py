"""
X Language Compiler
"""
import click

from .tools.tokenizer import tokenize


def get_content(file):
    """
    Return the content of a file
    """
    content = None
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# Arguments
@click.argument('file', nargs=1, type=click.Path(exists=True))
# Options
# Commands
@click.command()
def xcc(file):
    """
    Main function of the Compiler
    """
    # Get the content of a given file
    content = get_content(file)
    # Convert the content in tokens
    tokens = []
    for token in tokenize(content):
        tokens.append(token)
