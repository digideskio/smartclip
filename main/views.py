from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from smartfile import OAuthClient

from smartclip.secrets import *
from main.models import User, Clipping
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
    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse('feed'))
    else:
        return redirect(reverse('home'))

@login_required
def view_clippings(request):
    clippings = Clipping.objects.filter(user=request.user)
    data = {'user': request.user, 'clippings': clippings}
    return render_to_response('view-clips.html',data,RequestContext(request))

@login_required
def clip_view(request):
    return HttpResponse('Clip View')

def logout_user(request):
    logout(request)
    return HttpResponse('Logged out')

def check_user(request):
    if request.user.is_authenticated():
        return HttpResponse('logged in')
    else:
        return HttpResponse('no user')
