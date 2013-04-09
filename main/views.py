from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from smartfile import OAuthClient

from smartclip.secrets import *
from main.auth import verify_user


def home(request):
    data = {'user': request.user}
    return render_to_response('main.html',data,RequestContext(request))

def oauth_redirect(request):
    api = OAuthClient(OAUTH_TOKEN, OAUTH_SECRET)
    token = api.get_request_token(callback=
            request.build_absolute_uri(reverse('authenticate')))
    request.session['REQUEST_TOKEN'] = token
    return redirect(api.get_authorization_url(token))

def authenticate(request):
    verifier = request.GET.get('verifier')
    api = OAuthClient(OAUTH_TOKEN, OAUTH_SECRET)

    try:
        request_token = request.session.pop('REQUEST_TOKEN')
    except:
        return redirect(reverse('oauth_redirect'))
    access_token = api.get_access_token(request_token, verifier=verifier)
    request.session['ACCESS_TOKEN'] = access_token
    return redirect(reverse('verify_login'))

def verify_login(request):
    try:
        access_token = request.session.pop('ACCESS_TOKEN')
    except KeyError:
        return redirect(reverse('home'))
    user = verify_user(access_token)
    import ipdb
    ipdb.set_trace()
    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse('feed'))
    else:
        return redirect(reverse('home'))

@login_required
def feed(request):
    return HttpResponse('You are logged in!')
