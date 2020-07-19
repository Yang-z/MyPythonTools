import json
import os.path

# Import file beyond the current file dir..
if __package__ is None or __package__ == '':
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from oauth.installed import login as oauth_login
else:
    from ..oauth.installed import login as oauth_login


with open(
    os.path.join(os.path.dirname(__file__), r".cache", r".json"), 
    'r', encoding='utf-8'
) as f:
    cache = json.loads(f.read())

def print_json(j):
    print(
        json.dumps(
            j,
            indent=4, separators=(',', ':'),
            ensure_ascii=False
        )
    )


class GFit:
    def __init__(self, google_account: str):
        self.google_account = google_account

        self.SERVICE = oauth_login(
            cache['API']['SERVICE_NAME'],  # "fitness"
            cache['API']['VERSION'],  # "v1"
            cache['API']['SCOPES'], 
            self.google_account
        )

    def list_dataSources(self):
        result = self.SERVICE.users().dataSources().list(
            userId = 'me'
        ).execute()
        print_json(result)

    def create_dataSources(self, data):
        result = self.SERVICE.users().dataSources().creat(
            userId = 'me',
            body = data
        ).execute()
        print_json(result)

    def get_datasets(self, dataSourceId, datasetId):
        result = self.SERVICE.users().dataSources().datasets().get(
            userId = 'me',
            dataSourceId = dataSourceId,
            datasetId = datasetId
        ).execute()
        print_json(result)

    def patch_datasets(self, dataSourceId, datasetId, body):
        result = self.SERVICE.users().dataSources().datasets().patch(
            userId = 'me',
            dataSourceId = dataSourceId,
            datasetId = datasetId,
            body = body
        ).execute()
        print_json(result)


# ref:
# http://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.html
# https://developers.google.com/fit/rest/v1/get-started
