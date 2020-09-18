import requests
import json
import hashlib
import vars

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

def sendingDel(url,message,headers={"Authorization":""}):
	response=requests.delete(url, headers=headers, json=message)
	data={"status_code":400, "content": json.loads(response.content)}
	if response.status_code == 200:
		data["status_code"]= 200
	return data

def sendingPut(url,message,headers={"Authorization":""}):
	response=requests.put(url, headers=headers, json=message)
	data={"status_code":400, "content": json.loads(response.content)}
	if response.status_code == 200:
		data["status_code"]= 200
	return data

def hashCreate(alg, file):
	algs=["sha224","sha256","sha384","sha512","whirlpool"]
	if (not alg in algs):
		return 0
	file_hash = hashlib.sha256()
	if alg == "sha224":
		file_hash = hashlib.sha224()
	elif alg == "sha256":
		file_hash = hashlib.sha256()
	elif alg == "sha384":
		file_hash = hashlib.sha384()
	elif alg == "sha512":
		file_hash = hashlib.sha512()
	elif alg == "whirlpool":
		file_hash = hashlib.whirlpool()
	else:
		return 0
	while True:
		fb = file.read(vars.BLOCK_SIZE)
		if not fb:
			break
		file_hash.update(fb.encode('utf-8'))
	return file_hash.hexdigest()

def parse(file):
	with open(file) as json_file:
		try:
			# json_data = file.read().encode('utf-8')
			return json.load(json_file)
		except ValueError as e:
			print('invalid json: %s' % e)
			return 0
