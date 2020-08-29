import os
import json

from common.Data import Data

# expected to be Singleton
class _Config:

    def __init__(self):
        self.data_dir = f"{os.environ.get('DATAPATH')}/for_google/drive"
        self._path_json: str = f"{self.data_dir}/config.json"
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
            self._json = Data.load(self._path_json)
        return self._json
 
    def save(self):
        Data.save(self._json, self._path_json)

    ################################################################################


config = _Config()

class _Cache:
    def __init__(self):
        # load from file
        self._TeamDriveDicts: dict = {}
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

    def Path_TDDict(self, user):
        path = Data.solve_path(
            config.json['Path_TeamDriveDict'], 
            {
                'appDataDir': config.data_dir,
                'user': user
            }
        )

        return path

    def TeamDriveDict(self, user)->dict:
        if self._TeamDriveDicts.get(user) is None:
            self._TeamDriveDicts[user] = Data.load(self.Path_TDDict(user))
        return self._TeamDriveDicts[user]

    def Save_TDDict(self, user):
        Data.save(self.TeamDriveDict(user), self.Path_TDDict(user))
    

cache = _Cache()


if __name__ == '__main__':
    service_name = config.json['API']['SERVICE_NAME']

    user0 = config.json['TDReceivers'][0]['email'].lower()
    tddic = cache.TeamDriveDict(user0)

    print("break here")
