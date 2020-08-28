import os
import json


_path_data = f"{os.environ.get('DATAPATH')}/for_google/drive"

# Python, just can't update a value by passing it to a function...
def _load(
        # in_memory_data,
        path, store_method='json'
):
    with open(path, 'r', encoding='utf-8') as f:
        fr = f.read()
        in_memory_data = json.loads(fr) \
            if store_method == 'json' \
            else eval(fr.lower())
    return in_memory_data

def _save(in_memory_data, path, store_method='json'):
    with open(path, 'w', encoding='utf-8') as f:
        if store_method == 'json':
            f.write(json.dumps(
                in_memory_data,
                indent=4, separators=(',', ':'),
                ensure_ascii=False
            ))
        else:
            f.write(str(in_memory_data))


# expected to be Singleton
class _config:

    def __init__(self):
        self._path_json: str = f"{_path_data}/config.json"
        self._json: dict = None

        self._json_eg = \
        {
            "API":
            {
                "SERVICE_NAME": "drive",
                "VERSION": "v3",
                "SCOPES":
                [
                    "https://www.googleapis.com/auth/drive"
                ]
            },

            "TDReceivers":
            [
                {
                    "email": "*@*.org",
                    "times": 0
                },
            ],

            "TDSources":
            [
                {
                    "org": "org.*",
                    "email": "*@*.org",
                    "org-name-zh": "*组织"
                },
            ],

            "TDSources_yx":
            [
                {
                    "org": "org.*",
                    "url": "https://*.workers.dev/drive",
                    "name-zh": "*组织",
                },
            ],

            "pyppeteer_args":
            {
                "default":
                {
                    "chromePath": "%LOCALAPPDATA%\\pyppeteer\\pyppeteer\\local-chromium\\575458\\chrome-win32",
                    "userDataDir": "%LOCALAPPDATA%\\pyppeteer\\pyppeteer\\.dev_profile\\tmp*"
                },
                "chromePath":"*\\chrome.exe",
                "userDataDir":"*\\User Data",
            },

            "requests_args":
            [
                {
                    "url": "https://drive.google.com/drive/u/0/shared-drives",
                    "headers":
                    {
                        "cookie": "...",
                        "upgrade-insecure-requests": "...",
                        "user-agent": "...",
                        "x-chrome-connected":"...",
                        "x-client-data":"..."
                    }
                },
                {
                    "url": "https://clients6.google.com/drive/v2internal/teamdrives",
                    "payload":
                        {
                            "fields": "kind,nextPageToken,items(...)",
                            "q": "hidden = false",
                            "key": "..."
                        },
                    "authorization": "..."
                }
            ]
        }

    ################################################################################
    @property
    def json(self) -> dict:
        if self._json is None:
            self._json = _load(self._path_json)
        return self._json

    # @json.setter
    # def json(self, value):
    #     if value is not None:
    #         self._json = value
    #     _save(self._json, self._path_json, 'json')

    ################################################################################

class _cache:
    def __init__(self):
        self._path_TeamDriveDict: str = f"{_path_data}/TeamDriveDict.json"

        # load from file
        self._TeamDriveDict: dict = None
        self._TeamDriveDict_eg = \
        {
            "<drive_id>":
            {
                "kind": "drive#teamDrive",
                "id": "<drive_id>",
                "name": "<drive_name>",
                "colorRgb": "#0f9d58",
                "...": "...",
            },
        }

        # only store on memory
        self.permissions: dict = {}

    @property
    def TeamDriveDict(self) -> dict:
        if self._TeamDriveDict is None:
            self._TeamDriveDict = _load(self._path_TeamDriveDict, 'json')
        return self._TeamDriveDict

    # @TeamDriveDict.setter
    # def TeamDriveDict(self, value):
    #     # what if value is None? The setter will save the original date to file!
    #     if value is not None:
    #         self._TeamDriveDict = value
    #     _save(self._TeamDriveDict, self._path_TeamDriveDict, 'json')
    def SaveTDDict(self):
        _save(self._TeamDriveDict, self._path_TeamDriveDict, 'json')
    

config = _config()
cache = _cache()


if __name__ == '__main__':
    print(config.json['API']['SERVICE_NAME'])
    print("break here")
