import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import available_attrs

import smartfile
from requests_oauthlib import OAuth1
from smartclip import secrets


class SmartfileClient(smartfile.OAuthClient):
    def _do_request(self, request, url, **kwargs):
        # I am subclassing OAuthClient here because I want plain old HTTP
        # responses.
        kwargs['auth'] = OAuth1(self._client.token,
                                client_secret=self._client.secret,
                                resource_owner_key=self._access.token,
                                resource_owner_secret=self._access.secret,
                                signature_method=smartfile.SIGNATURE_PLAINTEXT)
        response = request(url, stream=True, **kwargs)

        if response.headers.get('content-type') == 'application/json':
            try:
                body = response.json()
            except ValueError:
                body = response.text
        else:
            body = response.raw
            
        return HttpResponse(body, status=response.status_code)
            
    
class Smartfile(object):
    def __init__(self, client_token=None, client_secret=None, *args, **kwargs):
        access_token = kwargs.get('access_token')
        access_secret = kwargs.get('access_secret')

        self.client = SmartfileClient(client_token=client_token,
                                      client_secret=client_secret,
                                      access_token=access_token,
                                      access_secret=access_secret)

    def authenticate(self, request):
        verifier = request.GET.get('verifier')
        request_token = request.session.pop('REQUEST_TOKEN')
        access_token = self.client.get_access_token(request_token,
                                                    verifier=verifier)
        user = self._verify_user()
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)

        # Stuff the access_token into the session
        request.session['ACCESS_TOKEN'] = access_token
        return user

    def authorize(self, token):
        return self.client.get_authorization_url(token)

    def oauth_token(self, request, callback):
        token = self.client.get_request_token(callback=callback)
        request.session['REQUEST_TOKEN'] = token
        return token

    def _verify_user(self, *args, **kwargs):
        auth_response = self.client.get("/whoami")
        user = None
        
        if auth_response.status_code == 200:
            body = json.loads(auth_response.content)
            user_dict = body['user']
            user, created = User.objects.get_or_create(
                username=user_dict['username'],
                first_name=user_dict['first_name'],
                last_name=user_dict['last_name']
            )

            if created:
                self._initialize_user()

        return user

    def _initialize_user(self):
        for path in ['', '/html', '/pdf']:
            userdir = '/smartclip%s' % path
            try:
                self.client.get('/path/info%s' % userdir)
            except:
                self.client.post('/path/oper/mkdir', path= userdir)

