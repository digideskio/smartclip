from smartfile import OAuthClient
from smartfile import APIError
from smartclip.secrets import *

def verify_user(access_token):
    token = access_token[0]
    secret = access_token[1]
    api = OAuthClient(client_token=OAUTH_TOKEN, client_secret=OAUTH_SECRET,
                      access_token=token, access_secret = secret)
    try:        
        api('/whoami')
        return True
    except APIError:
        return False
