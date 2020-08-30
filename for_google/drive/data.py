import os

from common.Data import Data

# expected to be Singleton
class _Config:

    def __init__(self):
        self.data_dir = f"{os.environ.get('DATAPATH')}/for_google/drive"
        self._path_json: str = f"{self.data_dir}/config.json"
        self._json: dict = None

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
            TDDict = Data.load(self.Path_TDDict(user))
            self._TeamDriveDicts[user] = TDDict if TDDict else {}
        return self._TeamDriveDicts[user]

    def Save_TDDict(self, user):
        Data.save(self.TeamDriveDict(user), self.Path_TDDict(user))

cache = _Cache()


if __name__ == '__main__':
    service_name = config.json['API']['SERVICE_NAME']

    user0 = config.json['TDReceivers'][0]['email'].lower()
    tddic = cache.TeamDriveDict(user0)

    print("break here")
