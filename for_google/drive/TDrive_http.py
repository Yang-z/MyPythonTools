"""
    failed
"""

import requests
import json

from for_google.drive.data import config

requests_args = config.json['requests_args']
url = requests_args[0]['url']
headers = requests_args[0]['headers']

s = requests.Session()
r = s.get(url, headers=headers)

print('connected')

url = requests_args[1]['url']
payload = requests_args[1]['payload']
# authorization = requests_args[1]['authorization']

r = s.options(url, params=json.dumps(payload))
r = s.get(url, params=payload)

print("done")
