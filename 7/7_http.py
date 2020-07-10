from requests_futures.sessions import FuturesSession
import json
import time


with open("./.cache/script.json", 'r') as f:
    script = json.loads(f.read())

# load Cookie
with open(f"{script['request']['headers']['Cookie']}", 'r') as f:
    script['request']['headers']['Cookie'] = f.read()

# load amf
for action in script['actions']:
    for i, amf in enumerate(action['amf']):
        with open(f"{script['amf_dir']}{amf}", 'rb') as f:
            action['amf'][i] = f.read()


if __name__ == '__main__':
    session_1 = FuturesSession()
    session_2 = FuturesSession()

    url = script['request']['url']
    headers = script['request']['headers']

    count = 0
    while(True):
        print(count)
        count += 1
        for action in script['actions']:
            rs = []
            session = session_1
            res = None
            for amf in action['amf']:
                headers['Content-Length'] = str(len(amf))
                res = session.post(url, headers=headers, data=amf)
                session = session_2 if session is session_1 else session_1
                # time.sleep(0.5)
                # res.result()
            res.result()
            time.sleep(action['delay'])
        # break

    print('done')
