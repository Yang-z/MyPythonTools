import os
import pickle
import hashlib


class tokenSaver:
    PATH_CACHE = f"{os.environ.get('DATAPATH')}/for_google/oauth"
    PATH_CLIENT_SECRETS = f"{PATH_CACHE}/client_secret.json"
    PATH_TOKEN_DIR = f"{PATH_CACHE}/token.pickle"

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

        path = f"{tokenSaver.PATH_TOKEN_DIR}/{file_name}"
        return path


if __name__ == '__main__':
    def test():
        tokenSaver
        print('break here')

    test()
