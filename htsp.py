import click
import json
import hashlib

import vars
import common

@click.group()
def htsp():
    pass

@htsp.command()
def health():
    """HTSP health systems status:

    curl --request GET --url https://api.3vidence.com/htsp/health
    """
    url=vars.eHost+'/htsp/health'
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))

@htsp.command()
def listKeys():
    """List API keys:

    curl --request GET --url https://api.3vidence.com//htsp/info
    --header 'authorization: YOUR_JWT'
    """
    url=vars.eHost+'/htsp/info'
    with open(vars.fileConf) as json_file:
        conf_data = json.load(json_file)
        headers={"Authorization":conf_data["jwt"]}
        response=common.sendingGet(url,headers)
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('file_sign', type=click.File('r'))
@click.argument('key_name')
@click.option('-h','--hash', default="sha256", help='Hash algorithm')
@click.option('-d','--desc', default="0545 cli", help='Description')
@click.option('-c','--cloud', default=True, help='Store signature on cloud')
def htsq(file_sign,key_name,hash,desc,cloud):
    """HTSQ sign a file:

    curl --request POST --url https://api.3vidence.com/htsp/htsq
    --header 'content-type: application/json'
    --data '{ "api_key": "YOUR_APIKEY", "algorithm":"YOUR_ALG_HASH","hash":"YOUR_HASH", "cloud": BOOL, "desc": "YOUR_DESCRIPTION"}'
    """
    url=vars.eHost+'/htsp/htsq'
    file_hash = hashlib.sha256()
    while True:
        fb = file_sign.read(vars.BLOCK_SIZE)
        if not fb:
            break
        file_hash.update(fb.encode('utf-8'))
    with open(vars.fileConf) as json_file:
        conf_data = json.load(json_file)
        message = {"api_key": conf_data[key_name], "algorithm": hash,
            "hash":file_hash.hexdigest(), "cloud": cloud,"desc": desc}
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('file_sign', type=click.File('r'))
@click.argument('id_hjws')
def getHjws(file_sign,id_hjws):
    """Get HJWS """
    int(id_hjws,16)
    url=vars.eHost+'/htsp/hjws/'+id_hjws
    response=common.sendingGet(url)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    file_hash = hashlib.sha256()
    while True:
        fb = file_sign.read(vars.BLOCK_SIZE)
        if not fb:
            break
        file_hash.update(fb.encode('utf-8'))
        if file_hash.hexdigest() != response["content"]["hash"]:
            print("Bad file sign")
        else:
            print(json.dumps(response["content"],indent=2))
