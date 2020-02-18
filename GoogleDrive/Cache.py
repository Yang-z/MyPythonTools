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

        self._root = os.path.dirname(__file__) + r"/.cache/"

        self._path_credentials = self._root + r"credentials.json"
        self._path_account = self._root + r"<google_account>/"
        self._file_token = r"token.pickle"

        # only store on memory
        self.permissions = {}

        self._path_TDSources = self._root + r"TDSources.txt"
        self._path_TDReceivers = self._root + r"TDReceivers.txt"
        self._path_TDSources_yx = self._root + r"TDSources_yx.txt"

        # [
        #     {
        #         'org': "edu.*",
        #         'url': "*@*.edu",
        #         'org-name-zh': "某某大学",
        #     },
        # ]
        self._TDSources: list = None

        # [
        #     {
        #         'email': "*@gmail.com",
        #         'times': 1
        #     },
        # ]
        self._TDReceivers: list = None

        # [
        #     {
        #         'org': "edu.*",
        #         'url': "https://*.*.workers.dev/drive",
        #         'name-zh': "某某大学",
        #     },
        # ]
        self._TDSources_yx: list = None

        self._path_TeamDriveDict = self._root + r"TeamDriveDict.json"
        self._TeamDriveDict: dict = None

        self._path_pyppeteer_args = self._root + r"pyppeteer_args.json"

        # {
        #     'chromePath': r'*\Google\Chrome\Application\chrome.exe',
        #     'userDataDir': r'*\User Data',
        #     'userDataDir1': r'*\User Data 1',
        #     'userDataDir2': r'*\User Data 2',
        # }
        self._pyppeteer_args: dict = None

    ################################################################################

    @property
    def root(self):
        return self._root

    @property
    def path_credentials(self):
        return self._path_credentials

    def path_account(self, google_account: str):
        path = self._path_account.replace(r"<google_account>", google_account)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def path_token(self, google_account: str):
        path_account = self.path_account(google_account)
        return path_account + self._file_token

    ################################################################################

    @property
    def TDSources(self):
        if self._TDSources is None:
            self._TDSources = self._load(self._path_TDSources, 'text')
        return self._TDSources

    @TDSources.setter
    def TDSources(self, value):
        self._TDSources = value
        self._save(self._TDSources, self._path_TDSources, 'test')

    @property
    def TDReceivers(self):
        if self._TDReceivers is None:
            self._TDReceivers = self._load(self._path_TDReceivers, 'text')
        return self._TDReceivers

    @TDReceivers.setter
    def TDReceivers(self, value):
        self._TDReceivers = value
        self._save(self._TDReceivers, self._path_TDReceivers, 'test')

    @property
    def TDSources_yx(self):
        if self._TDSources_yx is None:
            self._TDSources_yx = self._load(self._path_TDSources_yx, 'text')
        return self._TDSources_yx

    @TDSources_yx.setter
    def TDSources_yx(self, value):
        self._TDSources_yx = value
        self._save(self._TDSources_yx, self._path_TDSources_yx, 'test')

    ################################################################################

    @property
    def TeamDriveDict(self):
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

    @property
    def pyppeteer_args(self):
        if self._pyppeteer_args is None:
            self._pyppeteer_args = self._load(self._path_pyppeteer_args, 'json')
        return self._pyppeteer_args

    # save to file when set
    @pyppeteer_args.setter
    def pyppeteer_args(self, args: dict):
        self._pyppeteer_args = args
        self._save(self._pyppeteer_args, self._path_pyppeteer_args, 'json')

    ################################################################################

    @staticmethod
    # Python, just can't update a value by passing it to a function...
    def _load(
            # in_memory_data,
            path, store_method='json'
    ):
        with open(path, 'r') as f:
            fr = f.read()
            in_memory_data = json.loads(fr) if store_method == 'json' else eval(fr.lower())
        return in_memory_data

    @staticmethod
    def _save(in_memory_data, path, store_method='json'):
        with open(path, 'w') as f:
            if store_method == 'json':
                f.write(json.dumps(in_memory_data, indent=4, separators=(',', ':')))
            else:
                f.write(str(in_memory_data))
                
    ################################################################################


cache = __Cache__()

if __name__ == '__main__':

    # tds = cache.TDSources
    # tdr = cache.TDReceivers
    # path_token = cache.path_token(cache.TDSources[0]['email'])

    # TeamDriveDict = cache.TeamDriveDict
    # TeamDriveDict['id'] = "item"

    print("done")
