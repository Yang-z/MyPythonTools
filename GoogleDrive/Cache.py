import os
import json


# expected to be Singleton
class __Cache__:

    def __init__(self):

        # print(os.path.abspath(".cache/"))
        # print(os.path.abspath("./.cache/"))
        # PyCharm figures it out right but Visual Studio Code doesn't, why?
        # Pycharm take the current file dir as the default work dir,
        # while VS Code take the opened dir as the default work dir.
        # print(os.getcwd())

        self._root: str = os.path.join(os.path.dirname(__file__), r".cache")

        self._path_json: str = os.path.join(self._root, "cache.json")
        self._json: dict = self._load(self._path_json)

        # load from file
        self._TeamDriveDict: dict = None

        # only store on memory
        self.permissions: dict = {}

    ################################################################################
    @property
    def json(self) -> dict:
        return self._json

    @json.setter
    def json(self, value):
        if value is not None:
            self._json = value
        self._save(self._json, self._path_json, 'json')

    ########################################
    """ interface """
    # "gd_api":
    # {
    #     "SCOPES":
    #     [
    #         "https://www.googleapis.com/auth/drive"
    #     ],
    #     "path_credentials": "<cache_root>/credentials.json",
    #     "path_token": "<cache_root>/<google_account>/token.pickle"
    # }

    @property
    def gd_api_SCOPES(self) -> list:
        return self._json["gd_api"]["SCOPES"]

    @property
    def gd_api_path_credentials(self) -> str:
        return self._solve_path(self._json["gd_api"]["path_credentials"])

    def gd_api_path_token(self, g_account: str) -> str:
        return self._solve_path(self._json["gd_api"]["path_token"], g_account)

    ########################################
    """ interface """
    # "pyppeteer_args":
    # {
    #     "default":
    #     {
    #         "chromePath": "%LOCALAPPDATA%\\pyppeteer\\pyppeteer\\local-chromium\\575458\\chrome-win32",
    #         "userDataDir": "%LOCALAPPDATA%\\pyppeteer\\pyppeteer\\.dev_profile\\tmp*"
    #     },
    #     "chromePath":"*\\chrome.exe",
    #     "userDataDir":"*\\User Data",
    # }
    @property
    def pyppeteer_args(self):
        return self._json["pyppeteer_args"]

    """ interface """
    # "requests_args":
    # [
    #     {
    #         "url": "https://drive.google.com/drive/u/0/shared-drives",
    #         "headers":
    #         {
    #             "cookie": "...",
    #             "upgrade-insecure-requests": "...",
    #             "user-agent": "...",
    #             "x-chrome-connected":"...",
    #             "x-client-data":"..."
    #         }
    #     },
    #     {
    #         "url": "https://clients6.google.com/drive/v2internal/teamdrives",
    #         "payload":
    #             {
    #                 "fields": "kind,nextPageToken,items(...)",
    #                 "q": "hidden = false",
    #                 "key": "..."
    #             },
    #         "authorization": "..."
    #     }
    # ]
    @property
    def requests_args(self):
        return self._json["requests_args"]

    ################################################################################
    """ interface """
    # "TDSources":
    # [
    #     {
    #         "org": "org.*",
    #         "email": "*@*.org",
    #         "org-name-zh": "*组织"
    #     },
    # ]
    @property
    def TDSources(self):
        return self._json["TDSources"]

    """ interface """
    # "TDReceivers":
    # [
    #     {
    #         "email": "@*.org",
    #         "times": 0
    #     },
    # ]
    @property
    def TDReceivers(self):
        return self._json["TDReceivers"]

    """ interface """
    # "TDSources_yx":
    # [
    #     {
    #         "org": "org.*",
    #         "url": "https://*.workers.dev/drive",
    #         "name-zh": "*组织",
    #     },
    # ],
    @property
    def TDSources_yx(self) -> dict:
        return self._json["TDSources_yx"]

    ########################################
    @property
    def _path_TeamDriveDict(self) -> str:
        return self._solve_path(self._json["path_TeamDriveDict"])

    """ interface """
    # {
    #     "<drive_id>":
    #     {
    #         "kind": "drive#teamDrive",
    #         "id": "<drive_id>",
    #         "name": "<drive_name>",
    #         "colorRgb": "#0f9d58",
    #         ...,
    #     },
    # }
    @property
    def TeamDriveDict(self) -> dict:
        if self._TeamDriveDict is None:
            self._TeamDriveDict = self._load(self._path_TeamDriveDict, 'json')
        return self._TeamDriveDict

    @TeamDriveDict.setter
    def TeamDriveDict(self, value):
        # what if value is None? The setter will save the original date to file!
        if value is not None:
            self._TeamDriveDict = value
        self._save(self._TeamDriveDict, self._path_TeamDriveDict, 'json')
    ################################################################################

    def _solve_path(self, raw_path: str, account: str = None) -> str:
        solved_path = raw_path.replace("<cache_root>", self._root)
        if account is not None:
            solved_path = solved_path.replace("<google_account>", account)

        # make sure the parent dir exists
        parent_dir = os.path.dirname(solved_path)
        if not os.path.isdir(parent_dir):  # if the dir exists or not
            os.makedirs(parent_dir)  # make the dir required
            print(f"{parent_dir} is created!")

        return solved_path

    @staticmethod
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

    @staticmethod
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
    ################################################################################


cache = __Cache__()

if __name__ == '__main__':

    # tds = cache.TDSources
    # tds1 = cache.json.TDSources  # error
    # email = cache.TDSources[0].email  # error

    # path_token = cache.path_token(cache.TDSources[0]['email'])

    # TeamDriveDict = cache.TeamDriveDict
    # cache.TeamDriveDict['id'] = "item test 测试"  # tested
    # cache.TeamDriveDict = None

    # print(f"{id(cache.TDSources)}, {id(cache.json['TDSources'])}")  # same

    print("done")
