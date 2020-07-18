import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from token_saver import tokenSaver

def login(
    # https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    API_SERVICE_NAME, API_VERSION,

    # https://developers.google.com/oauthplayground
    API_SCOPES,

    #
    email = None
):
    require_userinfo(API_SCOPES)
    API_SCOPES.sort()

    creds = tokenSaver.load(email, API_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(tokenSaver.PATH_CLIENT_SECRETS, API_SCOPES)
            creds = flow.run_local_server(port=0)

            email_linked = get_userinfo(creds)['email']
            if email is not None and email != email_linked:
                print("Account connected seems unmatch the one expected!")
            email = email_linked

        tokenSaver.save(email, API_SCOPES, creds)

    service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    return service


def require_userinfo(API_SCOPES: list):
    scopes_require = [
        'https://www.googleapis.com/auth/userinfo.email', 
        'https://www.googleapis.com/auth/userinfo.profile', 
        'openid'
    ]
    for s in scopes_require:
        if s not in API_SCOPES:
            API_SCOPES.append(s)

def get_userinfo(creds):
    service = build('oauth2', 'v2', credentials=creds)
    userinfo = service.userinfo().get().execute()
    print(json.dumps(
        userinfo,
        indent=4, separators=(',', ':'),
        ensure_ascii=False
    ))
    return userinfo

# deprecated
def connect(
    # https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    API_SERVICE_NAME, API_VERSION,
    
    # If modifying these scopes, delete the file token.pickle.
    API_SCOPES,

    # 
    PATH_CLIENT_SECRETS, 
    
    #
    PATH_TOKEN_PICKLE
    ):

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PATH_TOKEN_PICKLE):
        with open(PATH_TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # If there are no (valid) credentials available, let the user log in.
        else:
            flow = InstalledAppFlow.from_client_secrets_file(PATH_CLIENT_SECRETS, API_SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(PATH_TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    return service


if __name__ == '__main__':
    login('fitness', 'v1', [
       "https://www.googleapis.com/auth/fitness.activity.read"
    ], None)

    print(0)
    