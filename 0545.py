#!/usr/bin/env python3

from auth import *
from htsp import *

@click.group()
def cli():
  pass

cli.add_command(auth)
cli.add_command(htsp)

if __name__ == '__main__':
    cli()
