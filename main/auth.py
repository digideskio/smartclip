from django.contrib.auth import login
from django.contrib.auth.models import User

from smartfile import OAuthClient
from smartfile import APIError
from smartclip.secrets import *


def verify_user(access_token):
    token = access_token[0]
    secret = access_token[1]
    api = OAuthClient(client_token=OAUTH_TOKEN, client_secret=OAUTH_SECRET,
                      access_token=token, access_secret = secret)
    try:
        user_dict = api('/whoami')['user']
        user = User.objects.get_or_create(username=user_dict['username'], 
                                          first_name=user_dict['first_name'],
                                          last_name=user_dict['last_name'])
        return user[0]
    except APIError:
        return False

def generate_api(request):
    access_token = request.session.get('ACCESS_TOKEN')
    token = access_token[0]
    secret = access_token[1]
    return OAuthClient(client_token=OAUTH_TOKEN, client_secret=OAUTH_SECRET,
                      access_token=token, access_secret = secret)

    
