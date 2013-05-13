from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from . import auth
from .models import Clipping
from .forms import ClippingForm, ShareForm
from .auth import (generate_api, create_smartfile_docs,
                   create_smartfile_dirs, create_link)

def home(request):
    data = {'user': request.user, 'login_url': settings.LOGIN_URL}
    return render_to_response('main.html',data,RequestContext(request))

def oauth_redirect(request):
    api = generate_api(request)
    callback = request.build_absolute_uri(reverse('authenticate'))
    token = api.oauth_token(request, callback)
    return redirect(api.authorize(token))

def authenticate(request):
    api = generate_api(request)
    user = api.authenticate(request)
    dest = reverse('view_clippings')
    if not user:
        dest = reverse('home')

    return redirect(dest)

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
    auth.create_smartfile_docs(request, clip_id)
        
    return HttpResponse('rendered documents')

@login_required
def form_view(request,clip_id):
    clip_obj = Clipping.objects.get(id=clip_id)
    if request.method == "POST":
        prev_title = clip_obj.filename
        form = ClippingForm(instance=clip_obj, data=request.POST)
        if form.is_valid():
            form.save()
            form.save_m2m()
            title = clip_obj.filename
            if title != prev_title:
                api = generate_api(request)
                create_smartfile_dirs(api)
                try:
                    for ext in ['pdf', 'html']:
                        src = '/smartclip/%s/%s.%s' % (ext, prev_title, ext)
                        dst = '/smartclip/%s/%s.%s' % (ext, title, ext)
                        api.client.post('/path/oper/rename', src=src, dst=dst)
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

@login_required
def sort_clips(request):
    sort_key = request.GET.get('sort_key')
    clippings = Clipping.objects.filter(user=request.user).order_by(sort_key)
    return render_to_response('clip-listing.html', {'clippings': clippings},
                                RequestContext(request))

    
@login_required
def pdf_view(request):
    clip_id = request.GET.get('clip_id')
    clip_obj = Clipping.objects.get(id=clip_id)
    filename = clip_obj.filename + '.pdf'
    api = auth.generate_api(request)
    response = api.client.get('/path/data/smartclip/pdf', filename)
    response.mimetype = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response    

def logout_user(request):
    logout(request)
    data = {'logged_out': True }
    return render_to_response('main.html', data, RequestContext(request))

def check_user(request):
    if request.user.is_authenticated():
        return HttpResponse('logged in')
    else:
        return HttpResponse('no user')

@login_required
def delete_clipping(request, clip_id):
    clip = Clipping.objects.get(user=request.user, id=clip_id)
    if clip:
        api = generate_api(request)
        try:
            api.client.post('/path/oper/remove',
                            path='/smartclip/pdf/'+clip.filename+'.pdf')
            api.client.post('/path/oper/remove',
                            path='/smartclip/html/'+clip.filename+'.html')
        except:
            pass
        clip.delete()
        return HttpResponse('deleted')
    else:
        return HttpResponse('not authorized')

@login_required
def share_form(request, clip_id):
    clip = Clipping.objects.get(user=request.user, id=clip_id)
    if clip:
        if request.method == "POST":
            form = ShareForm(request.POST)
            if form.is_valid():
                api = generate_api(request)
                resp = create_link(api, clip.filename, **form.cleaned_data)
                if resp.get('href', None):
                    return HttpResponse('success')
                else:
                    return HttpResponse('failure')
            else:
                return render_to_response('share-form.html',
                                          {'form':form, 'clip_id': clip_id},
                                          RequestContext(request))
        else:
            form = ShareForm()
            return render_to_response('share-form.html',
                                  {'form':form, 'clip_id': clip_id},
                                  RequestContext(request))
    else:
        HttpResponse('not authorized')
