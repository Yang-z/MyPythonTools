from __future__ import print_function
import pickle
import os.path
import uuid

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import time

# from retrying import retry

# from Cache import cache
# it runs, but can't get linked in pyCharm, unless...

from .Cache import cache


class GDrive:

    def __init__(self, google_account: str, org_r: str = None):
        self.google_account = google_account
        self.org_r = org_r

        self.SERVICE = self.connect()

    def connect(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = cache.gd_api_SCOPES
        path_credentials = cache.gd_api_path_credentials
        path_token = cache.gd_api_path_token(self.google_account)

        # Call the Drive v3 API
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

    ################################################################################

    # Call the Drive v3 API
    def create_t_drive(self, name=None):
        if name is None:
            name = 'Untitled shared drive'

        drive_metadata = {
            'name': name,
            # "hidden": True
        }
        request_id = str(uuid.uuid4())
        # Call the Drive v3 API
        drive = self.SERVICE.drives().create(
            body=drive_metadata,
            requestId=request_id,
            fields='id'
        ).execute()
        print(f"create_t_drive: {drive}")
        return drive

    # Call the Drive v3 API
    def get_t_drive(self, drive_id):
        results = self.SERVICE.teamdrives().get(
            teamDriveId=drive_id,
            fields='*',
            # supportsTeamDrives=True,
        ).execute()
        print(f"get_t_drive({drive_id}): {results}")

    # Call the Drive v3 API
    def rename_t_drive(self, drive: dict, new_name: str):
        if drive['name'] == new_name:
            print(f"rename_t_drive: {drive['name']} == {new_name}")
            return

        body = {
            'name': new_name,
        }
        drive_updated = self.SERVICE.drives().update(
            driveId=drive['id'],
            body=body,
        ).execute()

        print(f"rename_t_drive: {drive['name']} => {new_name} ")

        return drive_updated

    # Call the Drive v3 API
    def is_drive_hidden(self, drive_id):
        result = self.SERVICE.drives().get(
            driveId=drive_id,
            fields="hidden, createdTime"
        ).execute()
        return result['hidden'], result['createdTime']

    # Call the Drive v3 API
    def hide_t_drive(self, drive_id):
        results = self.SERVICE.drives().hide(
            driveId=drive_id,
            fields='id, hidden'
        ).execute()
        print(f"hide_t_drive: {drive_id}, {results}")
        return results

    # Call the Drive v3 API
    def list_t_drives(self, page_size=100, page_token=None):
        response = self.SERVICE.drives().list(
            fields="nextPageToken, drives(id, name)",
            pageSize=page_size,
            pageToken=page_token,
            # useDomainAdminAccess=True,
            # q="'hidden'= True",
        ).execute()
        drives = response.get('drives', [])
        next_page_token = response.get('nextPageToken', None)

        print(f'list_t_drives: {len(drives)}')
        # for drive in drives:
        #    print(f" *{drive}")
        print(f"    *nextPageToken: {next_page_token}")

        return drives, next_page_token

    def yield_t_drive_1_by_1(self, page_size=10):
        drives: list = None
        next_page_token = None
        while(drives == None or next_page_token != None):
            drives, next_page_token = self.list_t_drives(page_size, next_page_token)
            for drive in drives:
                yield drive  # amazing!

    ################################################################################
    
    # Call the Drive v3 API
    def list_permissions(self, drive_id):
        results = self.SERVICE.permissions().list(
            fileId=drive_id,
            supportsTeamDrives=True,
            fields='*'
        ).execute()
        items = results.get('permissions', [])

        print('list_permissions:')
        for item in items:
            print(f"    *{item}")

        return items

    def get_permission_by_email(self, drive_id, email):
        permissions = self.list_permissions(drive_id)
        for permission in permissions:
            if permission['emailAddress'] == email:
                return permission
        return None

    # Use cache.permissions if exists
    def get_permission_id_by_email(self, drive_id, email):
        if email in cache.permissions:
            return cache.permissions[email]
        else:
            permission_id = self.get_permission_by_email(drive_id, email)['id']
            cache.permissions[email] = permission_id
            return permission_id

    # Call the Drive v3 API
    def create_permission(self, drive_id, email, role='organizer'):
        body = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        results = self.SERVICE.permissions().create(
            body=body,
            fileId=drive_id,
            supportsTeamDrives=True,
            sendNotificationEmail=False,
            # fields='*'
        ).execute()

        print(f"create_permission: {results}")
        return results

    # Call the Drive v3 API
    def delete_permission(self, drive_id, permission_id):
        results = self.SERVICE.permissions().delete(
            fileId=drive_id,
            permissionId=permission_id,
            supportsTeamDrives=True,
            # fields='*'
        ).execute()

        print(f"delete_permission(d_id:{drive_id}, p_id:{permission_id}): {results}")  # nothing
        return results

    ################################################################################

    def create_t_drive_for(self, to_email, name=None):
        drive = self.create_t_drive(name)
        self.create_permission(drive['id'], to_email)
        creator_permission_id = self.get_permission_id_by_email(drive['id'], self.google_account)
        self.delete_permission(drive['id'], creator_permission_id)

    # Use cache.TeamDrive to obtain org
    def rename_t_drive_by_org(self, drive):
        try:
            org: str = cache.TTeamDriveDictesmDriveDict[drive['id']]['primaryDomainName']
        except Exception as e:
            print(f"Drive({drive['id']}, {drive['name']}) is not found in cache!!!] ")
            return
        
        org_list: list = org.split('.')
        org_list.reverse()
        org_reversed = '.'.join(org_list)

        self.rename_t_drive(drive, org_reversed)

    ################################################################################
    def batch_hide_t_drive(self):
        print("batch_hide_t_drive: ")
        for drive in self.yield_t_drive_1_by_1():
            is_hidden, created_time = self.is_drive_hidden(drive['id'])
            print(f"drive[{drive['id']}]: {is_hidden}, {created_time}")
            if is_hidden:
                continue
            hide_result = self.hide_t_drive(drive['id'])
            print(f"batch_hide_t_drive: {hide_result}")

    def batch_trans_t_drive_to(self, to_email):
        drives, _ = self.list_t_drives(100) # could use yield func

        for drive in drives:
            permissions = self.list_permissions(drive['id'])
            if len(permissions) == 1 and drive['name'] == "Untitled shared drive":
                self.create_permission(drive['id'], to_email)

        time.sleep(3)

        for drive in drives:
            permissions = self.list_permissions(drive['id'])
            if len(permissions) == 2 and drive['name'] == "Untitled shared drive":
                permission_id = self.get_permission_id_by_email(drive['id'], self.google_account)
                self.delete_permission(drive['id'], permission_id)

    def batch_create_t_drive_for(self, to_email, name=None, times=8*1024):
        i = 0
        while i < times:
            print(f"batch_create_t_drive_for: {i}")
            self.create_t_drive_for(to_email, name)
            i = i + 1

    ################################################################################

    # Use cache.TDReceivers
    def batch_create_t_drive_1_4_all(self, name=None):
        # take org(reversed) for the drive name if name is not provided.
        drive_name = name if name is not None else self.org_r

        for receiver in cache.TDReceivers:
            times = receiver['times']
            to_email = receiver['email']

            while times > 0:
                print(f'{to_email}: {times}')
                self.create_t_drive_for(to_email, drive_name)
                times -= 1

    def batch_rename_t_drive_by_org(self):
        for drive in self.yield_t_drive_1_by_1():
            self.rename_t_drive_by_org(drive)
  
    ################################################################################

    # Use cache.TeamDrive to obtain org
    def batch_create_permission_for_when_org_is(self, email, org):

        for drive in self.yield_t_drive_1_by_1():
            try:
                _org: str = cache.TTeamDriveDictesmDriveDict[drive['id']]['primaryDomainName']
            except Exception as e:
                print(f"Drive({drive['id']}, {drive['name']}) is not found in cache!!!] ")
                continue

            if _org == org:
                self.create_permission(drive['id'], email)

    # Use cache.TeamDrive to obtain org
    def batch_delete_permission_for_when_org_is(self, email, org):
        for drive in self.yield_t_drive_1_by_1():
            try:
                _org: str = cache.TTeamDriveDictesmDriveDict[drive['id']]['primaryDomainName']
            except Exception as e:
                print(f"Drive({drive['id']}, {drive['name']}) is not found in cache!!!] ")
                continue

            if _org == org:
                permissions = self.list_permissions(drive['id'])
                if len(permissions) <= 1:
                    continue
                p_id = self.get_permission_id_by_email(drive['id'], email)
                self.delete_permission(drive['id'], p_id)

    ################################################################################

    # Use cache.TeamDriveDict ONLY
    def count_t_drive_by_org(self):
        statistics = {}

        for item in cache.TTeamDriveDictesmDriveDict:
            org = cache.TTeamDriveDictesmDriveDict[item]['primaryDomainName']
            if org not in statistics:
                statistics[org] = 1
            else:
                statistics[org] += 1

        for item in statistics:
            print(f"{item}: {statistics[item]}")

    # online
    def count_t_drive_by_name(self):
        statistics = {}

        for drive in self.yield_t_drive_1_by_1():
            name = drive['name']
            if name not in statistics:
                statistics[name] = 1
            else:
                statistics[name] += 1

        for item in statistics:
            print(f"{item}: {statistics[item]}")

########################################################################################################################


if __name__ == '__main__':

    GDriveSession1 = GDrive(cache.TDReceivers[0]['email'])
    for drive in GDriveSession1.yield_t_drive_1_by_1():
        print(drive)

    print('done!')
