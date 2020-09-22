import click
import json
import hashlib

import vars
import common

@click.group()
def delete():
    pass

@delete.command()
@click.argument('key_name')
def key(key_name):
    """Delete a key
    """
    url=vars.eHost+'/htsp/branch'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    if (not key_name in conf_data):
        print("Bad key name")
        return
    message = {"kid": conf_data[key_name].split('.')[0]}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))


@delete.command()
@click.argument('subject')
def subject(subject):
    """Delete a subject
    """
    url=vars.eHost+'/htsp/subject'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    if (not subject in conf_data):
        print("Bad subject name")
        return
    message = {"id_sec": conf_data[subject]["id_sec"]}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))

@delete.command()
def account():
    """Delete a account
    """
    url=vars.eHost+'/htsp/account'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("You need to login first")
        return
    message = {}
    headers={"Authorization":conf_data["jwt"]}
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
