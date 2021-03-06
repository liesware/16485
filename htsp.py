import click
import json
import hashlib

import vars
import common
import os

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
@click.option('-s','--suite', default="ed25519+rsa", help='Suite algorithm ["ed25519+dilithium2","ed25519+rsa"]')
@click.argument('email')
def branch(email,suite):
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
    if (not email in conf_data["subject"]):
        print("Bad subject")
        return
    if (not "branch" in conf_data):
        print("You need to init first")
        return
    if (not isinstance(conf_data["branch"],dict)):
        print("Bad branches")
        return
    if (not email in conf_data):
        print("You need to verify your subject")
        return
    if (not isinstance(conf_data[email],list)):
        print("You need to init first")
        return
    branch = input("Your branch name: ")
    if (branch in conf_data["branch"]):
        print("Branch already exists")
        return
    message = {"id_sec": conf_data["subject"][email],"branch":branch, "suite": suite}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data["branch"][branch]= response["content"]["api_key"]
    conf_data[email].append(branch)
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Branch OK!")


@htsp.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('r'),nargs=-1)
def deletef(key_name,file_sign):
    """Delete a cloud hjws with a _hjws.json file
    """
    url=vars.eHost+'/htsp/hjws'
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
            print("Bad config file")
            return
        if (not "id_hjws" in data):
            print("Bad id_hjws")
            return
        message = {"api_key": conf_data["branch"][key_name], "id_hjws": data["id_hjws"]}
        response=common.sendingDel(url,message)
        if response["status_code"] != 200:
            print('\n'+i.name)
            print(json.dumps(response["content"],indent=2))
            return
        print('\n'+i.name)
        print(json.dumps(response["content"],indent=2))
        os.remove(i.name)

@htsp.command()
@click.argument('key_name')
@click.argument('id_hjws',nargs=-1)
def delete(key_name,id_hjws):
    """Delete a cloud hjws with a id_hjws
    """
    url=vars.eHost+'/htsp/hjws'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in id_hjws:
        message = {"api_key": conf_data["branch"][key_name], "id_hjws": i}
        response=common.sendingDel(url,message)
        print('\n'+i)
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('file_sign', type=click.File('r'),nargs=-1)
def get(file_sign):
    """Get a cloud id_hjws
    """
    for i in file_sign:
        data = common.parse(i.name)
        if not data:
            print("Bad hjws file")
            return
        if (not "id_hjws" in data):
            print("Bad id_hjws")
            return
        url=vars.eHost+'/htsp/hjws/'+data["id_hjws"]
        response=common.sendingGet(url)
        print('\n'+i.name)
        print(json.dumps(response["content"],indent=2))


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
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    message = {"api_key": conf_data["branch"][key_name]}
    response1=common.sendingPost(url,message)
    url=vars.eHost+'/htsp/pubkey/'+conf_data["branch"][key_name].split('.')[0]
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
    email = conf_data["email"]
    message = {"subject": email, "type": "email"}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] == 200:
        conf_data["subject"]= {conf_data["email"]:response["content"]["id_sec"]}
        with open(vars.fileConf, 'w') as outfile:
            json.dump(conf_data, outfile,indent=2)
    code = input("Your email verification code: ")
    url=vars.eHost+'/htsp/verification/'+code
    response=common.sendingGet(url,headers)
    print(json.dumps(response["content"],indent=2))
    if response["status_code"] != 200:
        print("Bad Verification code")
        return
    if (not conf_data["subject"][conf_data["email"]]):
        print("Subject error")
        return
    url=vars.eHost+'/htsp/branch'
    branch = input("Your branch name: ")
    if ("branch" in conf_data):
        if(branch in conf_data["branch"]):
            print("This branch already exists")
            return
    message = {"id_sec": conf_data["subject"][conf_data["email"]],"branch":branch}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    if (not "branch" in conf_data):
        conf_data["branch"]= {branch:response["content"]["api_key"]}
    elif (isinstance(conf_data["branch"],dict)):
        conf_data["branch"][branch]= response["content"]["api_key"]
    else:
        conf_data["branch"]= {branch:response["content"]["api_key"]}
    if(not email in conf_data):
        conf_data[email]=[branch]
    elif (isinstance(conf_data[email],list)):
        conf_data[email].append(branch)
    else:
        conf_data[email]=[branch]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Init OK!")


@htsp.command()
@click.argument('file_sign', type=click.File('rb'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512"]')
def search(file_sign,hash):
    """search a file by hash
    """
    url=vars.eHost+'/htsp/hash'
    for i in file_sign:
        file_hash = common.hashCreate(hash,i)
        if(file_hash==0):
            print("Bad algorithm")
            return
        message = {"hash": file_hash}
        response=common.sendingPost(url,message)
        print('\n'+i.name)
        print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('key_name')
@click.argument('file_sign', type=click.File('rb'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512"]')
@click.option('-d','--desc', default="0545 cli", help='Description')
@click.option('-c','--cloud', default=True, help='Store signature on cloud [True/False]')
def sign(file_sign,key_name,hash,desc,cloud):
    """Sign a file
    """
    url=vars.eHost+'/htsp/htsq'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    for i in file_sign:
        file_hash = common.hashCreate(hash,i)
        if(file_hash==0):
            print("Bad algorithm")
            return
        if (cloud == "False"):
            cloud = False
        else:
            cloud = True
        message = {"api_key": conf_data["branch"][key_name], "algorithm": hash,
            "hash":file_hash, "cloud": cloud,"desc": desc}
        response=common.sendingPost(url,message)
        if response["status_code"] != 200:
            print('\n'+i.name)
            print(json.dumps(response["content"],indent=2))
            return
        print("File signed OK!",i.name)
        with open(i.name+'_hjws.json', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)


@htsp.command()
@click.argument('file_sign', type=click.File('rb'),nargs=-1)
@click.option('-h','--hash', default="sha256", help='Hash algorithm ["sha224","sha256","sha384","sha512"]')
def sign_anon(file_sign,hash):
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
            print('\n'+i.name)
            print(json.dumps(response["content"],indent=2))
            return
        print("File signed OK!: ", i.name)
        with open(i.name+'_hjws.json', 'w') as outfile:
            json.dump(response["content"], outfile,indent=2)


@htsp.command()
@click.argument('email')
def subject(email):
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
    if (not "subject" in conf_data):
        print("You need to init first")
        return
    if (not isinstance(conf_data["subject"],dict)):
        print("Bad subject")
        return
    code = email
    message = {"subject": code, "type": "email"}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPost(url,message,headers)
    if (not email in conf_data):
            conf_data[email]=[]
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data["subject"][email] = response["content"]["id_sec"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print(response["content"])
    code = input("Your email verification code: ")
    url=vars.eHost+'/htsp/verification/'+code
    response=common.sendingGet(url,headers)
    print(json.dumps(response["content"],indent=2))

@htsp.command()
@click.argument('key_name')
def update(key_name):
    """Update API KEY credentials
    """
    url=vars.eHost+'/htsp/apikey'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    message = {"api_key": conf_data["branch"][key_name]}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingPut(url,message,headers)
    conf_data["branch"][key_name]= response["content"]["api_key"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("API updated OK!")


@htsp.command()
@click.argument('file_sign', type=click.File('rb'),nargs=-1)
def verify(file_sign):
    """Verify a file
    """
    for i in file_sign:
        print('\n'+i.name)
        message = common.parse(i.name+'_hjws.json')
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
