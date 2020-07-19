import os.path
import pickle
import hashlib


class tokenSaver:
    PATH_CACHE = os.path.join(os.path.dirname(__file__), r".cache")
    PATH_CLIENT_SECRETS = os.path.join(PATH_CACHE, r"client_secret.json")
    # PATH_TOKEN_DIR = os.path.join(PATH_CACHE, r"token.pickle")

    @staticmethod
    def load(email, SCOPES):
        if email is None:
            return None

        creds = None
        PATH_TOKEN_PICKLE = tokenSaver.get_token_path(email, SCOPES)
        if os.path.exists(PATH_TOKEN_PICKLE):
            with open(PATH_TOKEN_PICKLE, 'rb') as token:
                creds = pickle.load(token)
        return creds

    @staticmethod  
    def save(email, SCOPES, credentials):
        PATH_TOKEN_PICKLE = tokenSaver.get_token_path(email, SCOPES)

        if not os.path.exists(os.path.dirname(PATH_TOKEN_PICKLE)):
            os.makedirs(os.path.dirname(PATH_TOKEN_PICKLE))
        
        with open(PATH_TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)

    @staticmethod
    def get_token_path(email, SCOPES: list):
        # SCOPES.sort()
        str_scopes = "\n".join(SCOPES)
        md = hashlib.md5()
        md.update(str_scopes.encode('utf-8'))
        file_name = email + "_" + md.hexdigest()

        path = os.path.join(tokenSaver.PATH_CACHE, r"token.pickle", file_name)
        return path
