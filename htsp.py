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
    """Health systems status
    """
    url=vars.eHost+'/htsp/health'
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('id_hjws',nargs=-1)
def hjws(id_hjws):
    """Get a cloud id_hjws
    """
    for i in id_hjws:
        url=vars.eHost+'/htsp/hjws/'+i
        response=common.sendingGet(url)
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('key_name')
@click.argument('id_hjws',nargs=-1)
def hjws_del(key_name,id_hjws):
    """Delete a cloud hjws
    """
    url=vars.eHost+'/htsp/hjws'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    for i in id_hjws:
        message = {"api_key": conf_data[key_name], "id_hjws": i}
        response=common.sendingDel(url,message)
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('r'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512","whirlpool"]')
@click.option('-d','--desc', default="0545 cli", help='Description')
@click.option('-c','--cloud', default=True, help='Store signature on cloud [True/False]')
def htsq(file_sign,key_name,hash,desc,cloud):
    """Sign a file
    """
    url=vars.eHost+'/htsp/htsq'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    for i in file_sign:
        file_hash = common.hashCreate(hash,i)
        if(file_hash==0):
            print("Bad algorithm")
            return
        message = {"api_key": conf_data[key_name], "algorithm": hash,
            "hash":file_hash, "cloud": cloud,"desc": desc}
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print("File signed OK!",i.name)
        with open(i.name+'.hjws', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)

@htsp.command()
@click.argument('file_sign', type=click.File('r'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512","whirlpool"]')
def htsq_anon(file_sign,hash):
    """Sign a file anonymously
    """
    url=vars.eHost+'/htsp/open/htsq'
    for i in file_sign:
        file_hash = common.hashCreate(hash,i)
        if(file_hash==0):
            print("Bad algorithm")
            return
        message = {"algorithm": hash,"hash":file_hash}
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print("File signed OK!: ", i.name)
        with open(i.name+'.hjws', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)

@htsp.command()
@click.argument('file_sign', type=click.File('r'),nargs=-1)
def htsr(file_sign):
    """Verify a file
    """
    for i in file_sign:
        message = common.parse(i.name+'.hjws')
        if not message:
            print("Bad json file: ", i.name)
            return
        if ("id_hjws" in message):
            url=vars.eHost+'/htsp/hjws/'+message["id_hjws"]
            response=common.sendingGet(url)
            if response["status_code"] != 200:
                url=vars.eHost+'/htsp/htsr'
                response=common.sendingPost(url, message)
                if response["status_code"] != 200:
                    print(json.dumps(response["content"],indent=2))
                    return
        else:
            url=vars.eHost+'/htsp/htsr'
            response=common.sendingPost(url, message)
            if response["status_code"] != 200:
                print(json.dumps(response["content"],indent=2))
                return
        file_hash = common.hashCreate(response["content"]["alg"],i)
        if(file_hash==0):
            print("Bad algorithm")
            return
        if file_hash != response["content"]["hash"]:
            print("Bad file sign")
        else:
            print(json.dumps(response["content"],indent=2))

# @htsp.command()
# @click.argument('file_sign', type=click.File('r'))
# @click.argument('id_hjws')
# def htsr_cloud(file_sign,id_hjws):
#     """Verify a file with a cloud id_hjws
#     """
#     url=vars.eHost+'/htsp/hjws/'+id_hjws
#     response=common.sendingGet(url)
#     if response["status_code"] != 200:
#         print(json.dumps(response["content"],indent=2))
#         return
#     file_hash = common.hashCreate(response["content"]["alg"],file_sign)
#     if(file_hash==0):
#         print("Bad algorithm")
#         return
#     if file_hash != response["content"]["hash"]:
#         print("Bad file sign")
#     else:
#         print(json.dumps(response["content"],indent=2))

@htsp.command()
def info():
    """Info account
    """
    url=vars.eHost+'/htsp/info'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingGet(url,headers)
    print(json.dumps(response["content"],indent=2))


@htsp.command()
@click.argument('key_name')
def info_key(key_name):
    """Info API key
    """
    url=vars.eHost+'/htsp/info/apikey'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    message = {"api_key": conf_data[key_name]}
    response1=common.sendingPost(url,message)
    url=vars.eHost+'/htsp/pubkey/'+conf_data[key_name].split('.')[0]
    response=common.sendingGet(url)
    response1["content"]["pubkey"] = response["content"]
    print(json.dumps(response1["content"],indent=2))


@htsp.command()
def init():
    """Init a new account
    """
    url=vars.eHost+'/htsp/subject'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "email" in conf_data):
        print("Bad 3vidence.json config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    message = {"subject": conf_data["email"],"type":"email"}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print("Subject already exists")
        return
    conf_data[conf_data["email"]]= response["content"]
    code = input("Your email verification code: ")
    url=vars.eHost+'/htsp/verification/'+code
    response=common.sendingGet(url,headers)
    if response["status_code"] != 200:
        print("Bad Verification code")
        return
    url=vars.eHost+'/htsp/branch'
    branch = input("Your branch name: ")
    message = {"id_sec": conf_data[conf_data["email"]]["id_sec"],"branch":branch}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data[branch]= response["content"]["api_key"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Init OK!")

@htsp.command()
@click.argument('key_name')
def key_upd(key_name):
    """Update API KEY credentials
    """
    url=vars.eHost+'/htsp/apikey'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    message = {"api_key": conf_data[key_name]}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPut(url,message,headers)
    conf_data[key_name]= response["content"]["api_key"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("API updated OK!")


@htsp.command()
def subject():
    """Create a subject
    """
    url=vars.eHost+'/htsp/subject'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    code = input("Your email: ")
    message = {"subject": code, "type": "email"}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data[code]= response["content"]
    code = input("Your email verification code: ")
    url=vars.eHost+'/htsp/verification/'+code
    response=common.sendingGet(url,headers)
    if response["status_code"] != 200:
        print("Bad Verification code")
        return
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Subject OK!")


@htsp.command()
@click.argument('email')
def branch(email):
    """Create a branch
    """
    url=vars.eHost+'/htsp/branch'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    if (not email in conf_data):
        print("Bad subject")
        return
    branch = input("Your branch name: ")
    message = {"id_sec": conf_data[email]["id_sec"],"branch":branch}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data[branch]= response["content"]["api_key"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Branch OK!")
