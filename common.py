import requests
import json

def sendingPost(url, message,headers={"Authorization":""}):
	response=requests.post(url, headers=headers, json=message)
	data={"status_code":400, "content": json.loads(response.content)}
	if response.status_code == 200:
		data["status_code"]= 200
	return data

def sendingGet(url,headers={"Authorization":""}):
	response=requests.get(url, headers=headers)
	data={"status_code":400, "content": json.loads(response.content)}
	if response.status_code == 200:
		data["status_code"]= 200
	return data
