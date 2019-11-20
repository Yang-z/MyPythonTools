from __future__ import print_function
import pickle
import os.path
import uuid

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


# Call the Drive v3 API
def connect(accout):
    path_credentials = r'.token/' + accout + r'/credentials.json'
    path_token = r'.token/' + accout + r'/token.pickle'

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
            flow = InstalledAppFlow.from_client_secrets_file(
                path_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_token, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service


def create_t_drive(SERVICE):
    drive_metadata = {
        'name': 'Untitled shared drive',
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


def hide_t_drive(SERVICE, id):
    results = SERVICE.drives().hide(
        driveId=id,
        fields='id, hidden'
    ).execute()
    # print(results)
    return results


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


def is_drive_hidden(SERVICE, id):
    result = SERVICE.drives().get(
        driveId=id,
        fields="hidden, createdTime"
    ).execute()
    return result['hidden'], result['createdTime']


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


def get_permission_by_email(SERVICE, id, email):
    permissions = list_permissions(SERVICE, id)
    for permission in permissions:
        if permission['emailAddress'] == email:
            print(permission)
            return permission
    return None


cache_permissions = {}


def get_permission_id_by_email(SERVICE, id, email):
    if email in cache_permissions:
        return cache_permissions[email]
    else:
        permission_id = get_permission_by_email(SERVICE, id, email)['id']
        cache_permissions[email] = permission_id
        return permission_id


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


def delete_permission(SERVICE, id, p_id):
    results = SERVICE.permissions().delete(
        fileId=id,
        permissionId=p_id,
        supportsTeamDrives=True,
        # fields='*'
    ).execute()

    print(results)
    return results


def create_t_drive_for(SERVICE, from_email, to_email):
    drive = create_t_drive(SERVICE)
    create_permission(SERVICE, drive['id'], to_email)
    creator_permission_id = get_permission_id_by_email(SERVICE, drive['id'], from_email)
    delete_permission(SERVICE, drive['id'], creator_permission_id)


if __name__ == '__main__':
    import time


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
            try:
                create_t_drive_for(SERVICE, from_email, to_email)
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
            i = i + 1


    # good idea, but need to reconstruct Funcs
    def try_and_sleep(Func, a, b):
        while True:
            try:
                r = Func(a, b)
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
            break
        return r


    def batch_hide_t_drive(SERVICE):
        count = 0
        while True:
            count += 1
            print(count)

            # drive = list_t_drives_1_by_1(SERVICE)
            while True:
                try:
                    drive = list_t_drives_1_by_1(SERVICE)
                except Exception as e:
                    print(e)
                    time.sleep(60)
                    continue
                break

            if drive is None:
                break
            else:
                # is_hidden = is_drive_hidden(SERVICE, drive['id'])
                while True:
                    try:
                        is_hidden, created_time = is_drive_hidden(SERVICE, drive['id'])
                    except Exception as e:
                        print(e)
                        time.sleep(60)
                        continue
                    break

                print("*", drive, "hidden:", is_hidden, "createdTime:", created_time)

                if is_hidden:
                    continue

                if drive['name'] != "Untitled shared drive":
                    print("**drive['name']: ", drive['name'])

                # result = hide_t_drive(SERVICE, drive['id'])
                while True:
                    try:
                        hide_result = hide_t_drive(SERVICE, drive['id'])
                    except Exception as e:
                        print(e)
                        time.sleep(60)
                        continue
                    break
                print("*", hide_result)


    while False:
        emails = {
            'from_email': "*****",
            'to_email': "*****",
        }
        f = open(r'.token/accounts.txt', 'w')
        f.write(str(emails))
        f.close()

        break

    while True:
        f = open(r'.token/accounts.txt', 'r')
        a = f.read()
        emails = eval(a)
        f.close()
        break

    # SERVICE = connect(emails['from_email'])
    # batch_trans_t_drive(SERVICE, emails['from_email'], emails['to_email'])
    # batch_create_t_drive_for(SERVICE, emails['from_email'], emails['to_email'])

    # SERVICE = connect(emails['to_email'])
    # batch_hide_t_drive(SERVICE)
