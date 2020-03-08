import requests
import json

with open("./.cache/request.json", 'r') as f:
    request = json.loads(f.read())

with open("./.cache/.amf", 'rb') as f:
    amf = f.read()

request['headers']['Content-Length'] = str(len(amf))

res = requests.post(request['url'], data=amf, headers=request['headers'])
print(res)
