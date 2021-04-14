import click
import json
import hashlib
import requests
import os

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
def post(file_sign,key_name,hash,desc):
    """Create a snippets signed
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
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in file_sign:
        data = common.parse(i.name)
        if not data:
            print("Bad json file: ", i.name)
            return
        message = {"api_key": conf_data["branch"][key_name],"data": data,"algorithm": hash,"desc": desc }
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print("Snippet OK!: ", i.name)
        with open(i.name+'_snpt.json', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)
        # url=vars.eHost+'/snippets/qr'
        # message = {"id_data": response["content"]["id_data"], "type": "api"}
        # response=requests.post(url,message)
        # if response.status_code != 200:
        #     print(response)
        #     return
        # with open(i.name+'.png', 'wb') as outfile:
        #     outfile.write(response.content)


@snippets.command()
@click.argument('key_name')
def info_key(key_name):
    """Info API key
    """
    url=vars.eHost+'/snippets/info'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    message = {"api_key": conf_data["branch"][key_name]}
    response=common.sendingPost(url,message)
    print(json.dumps(response["content"],indent=2))


@snippets.command()
@click.argument('file_sign', type=click.File('r'),nargs=-1)
def get(file_sign):
    """Get a snippet
    """
    for i in file_sign:
        print('\n'+i.name)
        message = common.parse(i.name)
        if not message:
            print("Bad json file: ", i.name)
            return
        if (not"id_data" in message):
            print("Bad snpt file: ", i.name)
            return
        url=vars.eHost+'/snippets/data/'+message["id_data"]
        response=common.sendingGet(url)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print(json.dumps(response["content"],indent=2))


@snippets.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('r'),nargs=-1)
def deletef(key_name,file_sign):
    """Delete a snippet
    """
    url=vars.eHost+'/snippets/id'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in file_sign:
        print('\n'+i.name)
        message = common.parse(i.name)
        if not message:
            print("Bad json file: ", i.name)
            return
        if (not"id_data" in message):
            print("Bad snpt file: ", i.name)
            return
        url=vars.eHost+'/snippets'
        message["api_key"] = conf_data["branch"][key_name]
        response=common.sendingDel(url, message)
        print('\n'+i.name)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print(json.dumps(response["content"],indent=2))
        os.remove(i.name)

@snippets.command()
@click.argument('key_name')
@click.argument('id_data',nargs=-1)
def delete(key_name,id_data):
    """Delete a cloud snippet with a id_data
    """
    url=vars.eHost+'/snippets'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in id_data:
        message = {"api_key": conf_data["branch"][key_name], "id_data": i}
        response=common.sendingDel(url,message)
        print('\n'+i)
        print(json.dumps(response["content"],indent=2))

@snippets.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('r'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512","whirlpool"]')
@click.option('-d','--desc', default="0545 cli", help='Description')
def update(file_sign,key_name,hash,desc):
    """Update snippets signed
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
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in file_sign:
        data = common.parse(i.name)
        if not data:
            print("Bad json file: ", i.name)
            return
        data2 = common.parse(i.name+'_snpt.json')
        if not data2:
            print("Bad json file: ", i.name)
            return
        if (not "id_data" in data2):
            print("Bad id_data")
            return
        message = {"api_key": conf_data["branch"][key_name], "id_data": data2["id_data"],"data": data,"algorithm": hash,"desc": desc }
        response=common.sendingPut(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print("Snippet OK!: ", i.name)
        with open(i.name+'_snpt.json', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)
