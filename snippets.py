import click
import json
import hashlib

import vars
import common

@click.group()
def snippets():
    pass

@snippets.command()
def health():
    """Health systems status
    """
    url=vars.eHost+'/snippets/health'
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))
