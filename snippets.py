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

@snippets.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('r'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512","whirlpool"]')
@click.option('-d','--desc', default="0545 cli", help='Description')
def data(file_sign,key_name,hash,desc):
    """Create an snippets signed
    """
    url=vars.eHost+'/snippets'
    algs=["sha224","sha256","sha384","sha512","whirlpool", "sha3_224","sha3_256","sha3_384","sha3_512"]
    if (not hash in algs):
        print("Bad algorithm")
        return 0
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    for i in file_sign:
        data = common.parse(i.name)
        if not data:
            print("Bad json file: ", i.name)
            return
        message = {"api_key": conf_data[key_name],"data": data,"algorithm": hash,"desc": desc }
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        with open(i.name+'.snpt', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)
