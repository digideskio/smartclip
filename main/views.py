from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import slugify 
from smartfile import OAuthClient

from smartclip.secrets import *
from smartclip.settings import MEDIA_URL, MEDIA_ROOT
from main.models import User, Clipping
from main.forms import ClippingForm
from main.auth import verify_user, generate_api, create_smartfile_docs


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
        access_token = request.session.get('ACCESS_TOKEN')
    except KeyError:
        return redirect(reverse('home'))
    user = verify_user(access_token)
    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse('view_clippings'))
    else:
        return redirect(reverse('home'))

@login_required
def view_clippings(request):
    clippings = Clipping.objects.filter(user=request.user)
    data = {'user': request.user, 'clippings': clippings}
    return render_to_response('view-clips.html', data,
                              RequestContext(request))

@login_required
def html_view(request):
    clip_id = request.GET.get('clip_id')
    clip = Clipping.objects.get(id=clip_id)
    data = {'clip_html': clip.html}
    return render_to_response('pdf_template.html', data, RequestContext(request))

@login_required
def render_documents(request):
    clip_id = request.GET.get('clip_id')
    create_smartfile_docs(request, clip_id)
        
    return HttpResponse('rendered documents')

@login_required
def form_view(request,clip_id):
    clip_obj = Clipping.objects.get(id=clip_id)
    if request.method == "POST":
        prev_title = slugify(clip_obj.title)
        form = ClippingForm(instance=clip_obj, data=request.POST)
        if form.is_valid():
            form.save()

            title = slugify(clip_obj.title)
            if title != prev_title:
                api = generate_api(request)
                try:
                    api.post('/path/oper/rename', src='/smartclip/pdf/'+prev_title+'.pdf',
                             dst='/smartclip/pdf/'+title+'.pdf')
                    api.post('/path/oper/rename', src='/smartclip/html/'+prev_title+'.html',
                             dst='/smartclip/html/'+title+'.html')
                except:
                    create_smartfile_docs(request, clip_id)
            return render_to_response('clip-listing.html', {'clippings': [clip_obj]},
                                      RequestContext(request))
        else:
            return render_to_response('form-template.html', {'form':form, 'clip_id':clip_id},
                                      RequestContext(request))
    else:
        form = ClippingForm(instance=clip_obj)
        return render_to_response('form-template.html', {'form':form, 'clip_id':clip_id},
                                  RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponse('Logged out')

def check_user(request):
    if request.user.is_authenticated():
        return HttpResponse('logged in')
    else:
        return HttpResponse('no user')
