from __future__ import print_function
import pickle
import os.path
import uuid

from retrying import retry

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


# Call the Drive v3 API
def connect(account):
    path_credentials = r'.cache/credentials.json'
    path_account = r'.cache/' + account
    if not os.path.exists(path_account):
        os.makedirs(path_account)
    path_token = path_account + r'/token.pickle'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_token):
        with open(path_token, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_token, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service


@retry(wait_random_min=30000, wait_random_max=60000)
def create_t_drive(SERVICE, name=None):
    if name is None:
        name = 'Untitled shared drive'

    drive_metadata = {
        'name': name,
        # "hidden": True
    }
    request_id = str(uuid.uuid4())
    # Call the Drive v3 API
    drive = SERVICE.drives().create(
        body=drive_metadata,
        requestId=request_id,
        fields='id'
    ).execute()
    print(drive)
    return drive


@retry(wait_random_min=30000, wait_random_max=60000)
def hide_t_drive(SERVICE, id):
    results = SERVICE.drives().hide(
        driveId=id,
        fields='id, hidden'
    ).execute()
    # print(results)
    return results


@retry(wait_random_min=30000, wait_random_max=60000)
def is_drive_hidden(SERVICE, id):
    result = SERVICE.drives().get(
        driveId=id,
        fields="hidden, createdTime"
    ).execute()
    return result['hidden'], result['createdTime']


@retry(wait_random_min=30000, wait_random_max=60000)
def list_t_drives(SERVICE):
    results = SERVICE.drives().list(
        #
    ).execute()
    items = results.get('drives', [])

    if not items:
        print('No drives found.')
    else:
        print('Permissions:')
        for item in items:
            print("*", item)

    return items


cache_response = None
cache_i = None
@retry(wait_random_min=30000, wait_random_max=60000)
def list_t_drives_1_by_1(SERVICE):
    global cache_response
    global cache_i

    if cache_i is None:
        response = SERVICE.drives().list(
            # useDomainAdminAccess=True,
            # q="'hidden'= True",
            pageSize=100,
            fields="nextPageToken, drives(id, name)",
            pageToken=cache_response.get('nextPageToken', None) if cache_response is not None else None
        ).execute()
        cache_response = response
        cache_i = 0

    list = cache_response.get('drives', [])

    if cache_i < len(list):
        drive = list[cache_i]
        cache_i += 1
        return drive

    else:
        cache_i = None
        if cache_response.get('nextPageToken', None) is None:
            cache_response = None
            return None
        else:
            return list_t_drives_1_by_1(SERVICE)


@retry(wait_random_min=30000, wait_random_max=60000)
def get_t_drive(SERVICE, id):
    results = SERVICE.teamdrives().get(
        teamDriveId=id,
        fields='*',
        # supportsTeamDrives=True,
    ).execute()
    print(results)


@retry(wait_random_min=30000, wait_random_max=60000)
def list_permissions(SERVICE, id):
    results = SERVICE.permissions().list(
        fileId=id,
        supportsTeamDrives=True,
        fields='*'
    ).execute()
    items = results.get('permissions', [])

    if not items:
        print('No permissions found.')
    else:
        print('Permissions:')
        for item in items:
            print(u'*{0} ({1}) ({2})'.format(item['emailAddress'], item['role'], item['id']))

    return items


@retry(wait_random_min=30000, wait_random_max=60000)
def get_permission_by_email(SERVICE, id, email):
    permissions = list_permissions(SERVICE, id)
    for permission in permissions:
        if permission['emailAddress'] == email:
            print(permission)
            return permission
    return None


cache_permissions = {}
@retry(wait_random_min=30000, wait_random_max=60000)
def get_permission_id_by_email(SERVICE, id, email):
    if email in cache_permissions:
        return cache_permissions[email]
    else:
        permission_id = get_permission_by_email(SERVICE, id, email)['id']
        cache_permissions[email] = permission_id
        return permission_id


@retry(wait_random_min=30000, wait_random_max=60000)
def create_permission(SERVICE, id, email):
    body = {
        'type': 'user',
        'role': 'organizer',
        'emailAddress': email
    }
    results = SERVICE.permissions().create(
        body=body,
        fileId=id,
        supportsTeamDrives=True,
        sendNotificationEmail=False,
        # fields='*'
    ).execute()

    print(results)
    return results


@retry(wait_random_min=30000, wait_random_max=60000)
def delete_permission(SERVICE, id, p_id):
    results = SERVICE.permissions().delete(
        fileId=id,
        permissionId=p_id,
        supportsTeamDrives=True,
        # fields='*'
    ).execute()

    print(results)  # nothing
    return results


def create_t_drive_for(SERVICE, from_email, to_email, name=None):
    drive = create_t_drive(SERVICE, name)
    create_permission(SERVICE, drive['id'], to_email)
    creator_permission_id = get_permission_id_by_email(SERVICE, drive['id'], from_email)
    delete_permission(SERVICE, drive['id'], creator_permission_id)


def rename_t_drive_by_org(SERVICE):
    drive = list_t_drives_1_by_1(SERVICE)
    
    return


########################################################################################################################
TDSources = []
TDReceivers = []
def load_accounts():
    global TDSources
    global TDReceivers

    while False:
        TDSources = [
            {
                'org': "edu.*",
                'url': "*@*.edu",
                'org-name-zh': "某某大学",
            },

        ]

        TDReceivers = [
            {
                'email': "*@gmail.com",
                'times': 1
            },

        ]

        with open(r'.cache/TDSources.txt', 'w') as f:
            f.write(str(TDSources))

        with open(r'.cache/TDReceivers.txt', 'w') as f:
            f.write(str(TDReceivers))

        break

    while True:
        with open(r'.cache/TDSources.txt', 'r') as f:
            TDSources = eval(f.read().lower())

        with open(r'.cache/TDReceivers.txt', 'r') as f:
            TDReceivers = eval(f.read().lower())

        break


########################################################################################################################
def batch_trans_t_drive(SERVICE, from_email, to_email):
    drives = list_t_drives(SERVICE)
    for drive in drives:
        permissions = list_permissions(SERVICE, drive['id'])
        if len(permissions) == 1:
            create_permission(SERVICE, drive['id'], to_email)

    for drive in drives:
        permissions = list_permissions(SERVICE, drive['id'])
        if len(permissions) == 2 and drive['name'] == "Untitled shared drive":
            permission_id = get_permission_id_by_email(SERVICE, drive['id'], from_email)
            delete_permission(SERVICE, drive['id'], permission_id)


def batch_create_t_drive_for(SERVICE, from_email, to_email):
    i = 8
    i_max = 10 + 24
    while i < i_max:
        print(i)
        create_t_drive_for(SERVICE, from_email, to_email)
        i = i + 1


def batch_hide_t_drive(SERVICE):
    count = 0
    while True:
        count += 1
        print(count)

        drive = list_t_drives_1_by_1(SERVICE)

        if drive is None:
            break
        else:
            is_hidden, created_time = is_drive_hidden(SERVICE, drive['id'])
            print("*", drive, "hidden:", is_hidden, "createdTime:", created_time)

            if is_hidden:
                continue

            if drive['name'] != "Untitled shared drive":
                print("**drive['name']: ", drive['name'])

            hide_result = hide_t_drive(SERVICE, drive['id'])
            print("*", hide_result)


########################################################################################################################
def batch_create_t_drives_1_for_all(td_source, td_receivers):
    from_email = td_source['email']
    service = connect(from_email)
    t_drive_name = td_source['org']

    for td_receiver in td_receivers:
        to_email = td_receiver['email']
        times = td_receiver['times']

        while times > 0:
            create_t_drive_for(service, from_email, to_email, t_drive_name)
            times -= 1


########################################################################################################################
if __name__ == '__main__':
    load_accounts()

    # from_email = TDSources[0]['email']
    # to_email = TDReceivers[-1]['email']

    # SERVICE = connect(from_email)
    # batch_trans_t_drive(SERVICE, from_email, to_email)
    # batch_create_t_drive_for(SERVICE, from_email, 'to_email')

    # SERVICE = connect(to_email)
    # batch_hide_t_drive(SERVICE)

    ################################################################

    # batch_create_t_drives_1_for_all(TDSources[1], TDReceivers)


