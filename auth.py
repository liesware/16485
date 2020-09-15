import click
import json
import hashlib

import vars
import common
import auth_curls

@click.group()
def auth():
    pass

@auth.command()
def curls():
    """Auth curls
    """
    auth_curls.api()


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
    with open(vars.fileConf) as json_file:
        conf_data = json.load(json_file)
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
def password_upd():
    """
    3vidence Signup
    """
    url=vars.eHost+'/auth/password'
    with open(vars.fileConf) as json_file:
        conf_data = json.load(json_file)
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
@click.argument('email')
def signup(email):
    """
    3vidence Signup
    """
    url=vars.eHost+'/auth/signup'
    message = {"email": email}
    response=common.sendingPost(url,message)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
    conf = response["content"]
    code = input("Your verification code: ")
    url=vars.eHost+'/auth/verification/'+code
    response=common.sendingGet(url)
    if response["status_code"] != 200:
        print(json.dumps(response["content"],indent=2))
        return
    print(json.dumps(response["content"],indent=2))
    with open(vars.fileConf, 'w') as outfile:
        json.dump(conf, outfile,indent=2)
