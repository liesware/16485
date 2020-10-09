import click
import json
import hashlib

import vars
import common
import os

@click.group()
def delete():
    pass

@delete.command()
@click.argument('key_name')
def branch(key_name):
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
    if (not "branch" in conf_data):
        print("You need to init first")
        return
    if (not isinstance(conf_data["branch"],dict)):
        print("Bad branches")
        return
    if (not key_name in conf_data["branch"]):
        print("Bad key name")
        return
    message = {"kid": conf_data["branch"][key_name].split('.')[0]}
    headers={"Authorization":conf_data["jwt"]}
    click.confirm('Do you want to continue?', abort=True)
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
    del conf_data["branch"][key_name]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)


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
    if (not subject in conf_data["subject"]):
        print("Bad subject name")
        return
    message = {"id_sec": conf_data["subject"][subject]}
    headers={"Authorization":conf_data["jwt"]}
    click.confirm('Do you want to continue?', abort=True)
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
    del conf_data["subject"][subject]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)

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
    click.confirm('Do you want to continue?', abort=True)
    response=common.sendingDel(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
    os.remove(vars.fileConf)
