#!/usr/bin/env python3

from auth import *
from htsp import *
from snippets import *
from delete import *

@click.group()
def cli():
  pass

cli.add_command(auth)
cli.add_command(htsp)
cli.add_command(snippets)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
