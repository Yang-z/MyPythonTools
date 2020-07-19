from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Import file in the current file dir.
if __name__ == '__main__':
    from token_saver import tokenSaver
else:
    from .token_saver import tokenSaver


def login(
    # https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    API_SERVICE_NAME, API_VERSION,

    # https://developers.google.com/oauthplayground
    # If modifying these scopes, the old file token.pickle becomes unsuitable.
    API_SCOPES,

    # If not provided, no stored token could be found.
    email = None
):
    require_userinfo(API_SCOPES)
    API_SCOPES.sort()

    creds = tokenSaver.load(email, API_SCOPES)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if not creds or not creds.valid:

        # refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # If there are no (valid) credentials available, let the user log in.
        else:
            flow = InstalledAppFlow.from_client_secrets_file(tokenSaver.PATH_CLIENT_SECRETS, API_SCOPES)
            creds = flow.run_local_server(port=0)

            # Get the authorized account info, with the purpose of storing tokens separately
            email_linked = get_userinfo(creds)['email']
            if email is not None and email != email_linked:
                print("Account connected seems unmatch the one expected!")
            email = email_linked

        # Save the credentials for the next run
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


import json
def get_userinfo(creds):
    # ref: 
    # http://googleapis.github.io/google-api-python-client/docs/dyn/oauth2_v2.html
    # https://stackoverflow.com/questions/24442668/google-oauth-api-to-get-users-email-address
    # api:
    # https://www.googleapis.com/oauth2/v2/userinfo
    # or https://developers.google.com/people/v1/profiles#protocol
    service = build('oauth2', 'v2', credentials=creds)
    userinfo = service.userinfo().get().execute()
    print(json.dumps(
        userinfo,
        indent=4, separators=(',', ':'),
        ensure_ascii=False
    ))
    return userinfo


# ref: 
# https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-installed.md
# https://developers.google.com/drive/api/v3/quickstart/python
