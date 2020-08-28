import requests
import json
from time import sleep

from for_google.drive.data import config


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
        print(f"{td_receiver['email']} ← {td_source['org']} (status: {r.status_code})")


def request_1_4_all(td_source):
    for td_receiver in config.json['TDReceivers']:
        request_1_4_1(td_source, td_receiver)


def request_all_4_1(td_receiver):
    for td_source in config.json['TDSources_yx']:
        request_1_4_1(td_source, td_receiver)


########################################################################################################################

if __name__ == '__main__':
    # request_1_4_all(config.json['TDSources_yx'][-1])
    print("done!")
