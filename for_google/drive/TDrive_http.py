"""
    failed
"""

import requests
import json

from .Cache import cache


url = cache.requests_args[0]['url']
headers = cache.requests_args[0]['headers']

s = requests.Session()
r = s.get(url, headers=headers)

print('connected')

url = cache.requests_args[1]['url']
payload = cache.requests_args[1]['payload']
# authorization = cache.requests_args[1]['authorization']

r = s.options(url, params=json.dumps(payload))
r = s.get(url, params=payload)

print("done")
