import click
import json
import hashlib

import vars
import common

@click.group()
def auth():
    pass


@auth.command()
def health():
    """Health systems status
    """
    url=vars.eHost+'/auth/health'
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))

@auth.command()
def login():
    """
    3vidence login
    """
    url=vars.eHost+'/auth/login'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "email" in conf_data) or (not "password" in conf_data):
        print("Bad email/password")
        return
    data = {"email": conf_data["email"],"password":conf_data["password"]}
    response=common.sendingPost(url,data)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data["jwt"] = response["content"]["jwt"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Login OK")


@auth.command()
def update():
    """
    3vidence password update
    """
    url=vars.eHost+'/auth/password'
    conf_data = common.parse(vars.fileConf)
    if not conf_data:
        print("Bad config file")
        return
    if (not "jwt" in conf_data):
        print("Bad key name")
        return
    headers={"Authorization":conf_data["jwt"]}
    message={"":""}
    response=common.sendingPut(url,message,headers)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    conf_data["password"]= response["content"]["password"]
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf_data, outfile,indent=2)
    print("Password updated")


@auth.command()
def signup():
    """
    3vidence Signup
    """
    code = input("Your verification code: ")
    url=vars.eHost+'/auth/verification/'+code
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))
