import requests
import json
from time import sleep


def request_1_4_1(td_source, td_receiver):
    payload = json.dumps({
        "teamDriveName": td_source['org'],
        "teamDriveThemeId": "random",
        "emailAddress": td_receiver['email']
    })

    times = td_receiver['times']
    while times > 0:
        r = requests.post(td_source['url'], data=payload)
        sleep(3)
        times -= 1
        print(td_receiver['email'], " ← ", td_source['org'], "(status:", r.status_code, ")")


def request_1_4_all(td_source):
    for td_receiver in TDReceivers:
        request_1_4_1(td_source, td_receiver)


def request_all_4_1(td_receiver):
    for td_source in TDSources:
        request_1_4_1(td_source, td_receiver)


if __name__ == '__main__':
    while False:
        TDSources = [
            {
                'org': "edu.*",
                'url': "https://*.*.workers.dev/drive",
                'name-zh': "某某大学",
            },

        ]

        TDReceivers = [
            {
                'email': "*@gmail.com",
                'times': 1
            },

        ]

        with open(r'.token/TDSources_yx.txt', 'w') as f:
            f.write(str(TDSources))

        with open(r'.token/TDReceivers.txt', 'w') as f:
            f.write(str(TDReceivers))

        break

    while True:
        with open(r'.token/TDSources_yx.txt', 'r') as f:
            TDSources = eval(f.read())

        with open(r'.token/TDReceivers.txt', 'r') as f:
            TDReceivers = eval(f.read())

        break

    # request_1_4_1(TDSources[-1], TDReceivers[-1])
    print("done!")
