import json
import os.path
# from typing import Generator

from for_google.oauth.installed import login as oauth_login


with open(
    f"{os.environ.get('DATAPATH')}/for_google/fitness/config.json",
    'r', encoding='utf-8'
) as f:
    config = json.loads(f.read())

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
        self.google_account = google_account.lower()

        self.SERVICE = oauth_login(
            config['API']['SERVICE_NAME'],  # "fitness"
            config['API']['VERSION'],       # "v1"
            config['API']['SCOPES'], 
            self.google_account
        )

    ################################################################################

    def list_dataSource(self):
        result = self.SERVICE.users().dataSources().list(
            userId='me'
        ).execute()
        print_json(result)
        return result

    def create_dataSource(self, body):
        result = self.SERVICE.users().dataSources().create(
            userId='me',
            body=body
        ).execute()
        print_json(result)
        return result

    def update_dataSource(self, dataSourceId, body=None):
        result = self.SERVICE.users().dataSources().update(
            userId='me',
            dataSourceId=dataSourceId,
            body=body
        ).execute()
        print_json(result)
        return result

    def delete_dataSource(self, dataSourceId):
        result = self.SERVICE.users().dataSources().delete(
            userId='me',
            dataSourceId=dataSourceId,
        ).execute()
        print_json(result)
        return result

    def get_dataset(self, dataSourceId, datasetId):
        result = self.SERVICE.users().dataSources().datasets().get(
            userId='me',
            dataSourceId=dataSourceId,
            datasetId=datasetId
        ).execute()
        print_json(result)
        print(len(result['point']))
        return result

    def patch_dataset(self, dataSourceId, datasetId, body):
        result = self.SERVICE.users().dataSources().datasets().patch(
            userId='me',
            dataSourceId=dataSourceId,
            datasetId=datasetId,
            body=body
        ).execute()
        # print_json(result)
        print(datasetId, ": ", len(body['point']))
        print(len(result['point']))  # , " + ", result['nextPageToken'])
        return result

    ################################################################################
    def patch_dataset_2(self, dataSourceId:str, points:list, minStartTimeNs:int, maxEndTimeNs:int):
        self.patch_dataset(
            dataSourceId,
            str(minStartTimeNs) + '-' + str(maxEndTimeNs),
            {
                "dataSourceId": dataSourceId,
                "minStartTimeNs": minStartTimeNs,
                "maxEndTimeNs": maxEndTimeNs,
                "point": points
            }
        )

    def patch_dataset_3(self, dataSourceId, points, trunks=1000):
        count = 0
        for p in points:
            if count == 0:
                minStartTimeNs = None
                maxEndTimeNs = None
                points_t = []

            startTimeNanos = p['startTimeNanos']
            endTimeNanos = p['endTimeNanos']
            if minStartTimeNs is None or minStartTimeNs > startTimeNanos:
                minStartTimeNs = startTimeNanos
            if maxEndTimeNs is None or maxEndTimeNs < endTimeNanos:
                maxEndTimeNs = endTimeNanos
            points_t.append(p)
            count += 1

            if count == trunks:
                self.patch_dataset_2(dataSourceId, points_t, minStartTimeNs, maxEndTimeNs)
                count = 0

        if count != 0:
            self.patch_dataset_2(dataSourceId, points_t, minStartTimeNs, maxEndTimeNs)
            count = 0


# ref:
# http://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.html
# https://developers.google.com/fit/rest/v1/get-started


if __name__ == '__main__':
    def test():
        user = config['user'][1]['email']

        gfit = GFit(user)

        gfit.list_dataSource()
        
        # gfit.update_dataSource(
        #     config['user'][1]['dataStreamIds'][2],
        #     config['data_sources'][0]
        # )

        # gfit.get_dataset(
        #     config['user'][1]['dataStreamIds'][2],
        #     '1518402035000000000-1593531633000000000'
        # )

    test()

    def import_from_a_health_2_g_fit_4_step_count():
        from for_google.fitness.apple_health_to_google_fit import AppleHealthToGoogleFit

        user = config['user'][1]['email']
        data_source = config['data_sources'][0]

        gfit = GFit(user)
        result = gfit.create_dataSource(data_source)
        dataStreamId = result['dataStreamId']
        # dataStreamId = config['user'][1]['dataStreamIds'][2]
        print(dataStreamId)

        a2g_fit = AppleHealthToGoogleFit.get_instance()
        gfit.patch_dataset_3(dataStreamId, a2g_fit.get_g_records_step_count())

    # import_from_a_health_2_g_fit_4_step_count()
