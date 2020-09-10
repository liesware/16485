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
    """Auth health systems status"""
    url=vars.eHost+'/auth/health'
    response=common.sendingGet(url)
    print(json.dumps(response["content"],indent=2))

@auth.command()
def login():
    """3vidence login"""
    url=vars.eHost+'/auth/login'
    with open(vars.fileConf) as json_file:
        conf_data = json.load(json_file)
        data = {"email": conf_data["email"],"password":conf_data["password"]}
        response=common.sendingPost(url,data)
        if response["status_code"] != 200:
            print(json.dumps(response["content"],indent=2))
            return
        print(json.dumps(response["content"],indent=2))
        conf_data["jwt"] = response["content"]["jwt"]
        with open(vars.fileConf, 'w') as outfile:
            json.dump(conf_data, outfile,indent=2)
