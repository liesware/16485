#!/usr/bin/env python3

import click
import requests
import json
import hashlib

eHost='https://api.3vidence.com'
BLOCK_SIZE = 65536

def sendingPost(url, message):
	response=requests.post(url, data=message)
	return response.content

def sendingGet(url,headers={"Authorization":""}):
	response=requests.get(url, headers=headers)
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

@cli.command(name='login')
def login():
    """3vidence login"""
    url=eHost+'/auth/login'
    with open('login.json') as json_file:
        data = json.load(json_file)
        respose=json.loads(sendingPost(url,data))
        print(json.dumps(respose,indent=2))
        with open('token.json', 'w') as outfile:
            json.dump(respose, outfile)

@cli.command(name='listKeys')
def listKeys():
    """List API keys"""
    url=eHost+'/htsp/info'
    with open('token.json') as json_file:
        data = json.load(json_file)
        headers={"Authorization":data["jwt"]}
        respose=json.loads(sendingGet(url,headers))
        print(json.dumps(respose,indent=2))


@cli.command(name='htsq')
@click.argument('file_sign', type=click.File('r'))
def htsq(file_sign):
    """HTSQ sign file"""
    url=eHost+'/htsp/htsq'
    file_hash = hashlib.sha256()
    while True:
        fb = file_sign.read(BLOCK_SIZE)
        if not fb:
            break
        file_hash.update(fb.encode('utf-8'))
    # print (file_hash.hexdigest())
    with open('apikeys.json') as json_file:
        data = json.load(json_file)
        message = {"api_key": data["F51.4"], "algorithm":"sha256","hash":file_hash.hexdigest(), "desc": "test"}
        respose=json.loads(sendingPost(url,message))
        print(json.dumps(respose,indent=2))




if __name__ == '__main__':
    cli()
