#!/usr/local/opt/python3/bin/python3

import click
import requests
import json
import hashlib

eHost='https://api.3vidence.com'
BLOCK_SIZE = 65536

def sendingPost(url, message):
	response=requests.post(url, data=message)
	return response.content

def sendingGet(url):
	response=requests.get(url)
	return response.content

@click.group()
def cli():
  pass

@cli.command(name='health')
def health():
    """HTSP health systems status"""
    url=eHost+'/htsp/health'
    respose=json.loads(sendingGet(url))
    print(json.dumps(respose,indent=2))

@cli.command(name='htsq')
@click.argument('file_sign', type=click.File('r'))
def htsq(file_sign):
    """HTSQ sign file"""
    file_hash = hashlib.sha256()
    while True:
        fb = file_sign.read(BLOCK_SIZE)
        if not fb:
            break
        file_hash.update(fb.encode('utf-8'))
    print (file_hash.hexdigest())

if __name__ == '__main__':
    cli()
