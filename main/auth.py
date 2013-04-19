import os
from cStringIO import StringIO
from django.template.loader import get_template
from django.template import Context
from wkhtmltopdf.utils import wkhtmltopdf
from django.contrib.auth import login
from django.contrib.auth.models import User

from smartfile import OAuthClient
from smartfile import APIError
from smartclip.secrets import *
from smartclip.settings import MEDIA_URL, MEDIA_ROOT

from main.models import *



def verify_user(access_token):
    token = access_token[0]
    secret = access_token[1]
    api = OAuthClient(client_token=OAUTH_TOKEN, client_secret=OAUTH_SECRET,
                      access_token=token, access_secret = secret)
    try:
        user_dict = api('/whoami')['user']
        user, created = User.objects.get_or_create(username=user_dict['username'], 
                                          first_name=user_dict['first_name'],
                                          last_name=user_dict['last_name'])
        if created:
            api.post('/path/oper/mkdir', path='/smartclip')
            api.post('/path/oper/mkdir', path='/smartclip/html')
            api.post('/path/oper/mkdir', path='/smartclip/pdf')
        return user, created
    except APIError:
        return False

def generate_api(request):
    access_token = request.session.get('ACCESS_TOKEN')
    token = access_token[0]
    secret = access_token[1]
    return OAuthClient(client_token=OAUTH_TOKEN, client_secret=OAUTH_SECRET,
                      access_token=token, access_secret = secret)

    
def create_smartfile_docs(request, clip_id):
    clip = Clipping.objects.get(id=clip_id)
    base_path = MEDIA_URL + clip.filename
    
    api = generate_api(request)
    api.post('/path/data/smartclip/html', file=(clip.filename+'.html',
             StringIO(clip.html.encode('utf-8'))))
    
    html_file = open(base_path+'.html', 'w')
    html_file.write(clip.html.encode('ascii','xmlcharrefreplace'))
    html_file.close()

    wkhtmltopdf(pages=[base_path+'.html'], output=base_path+'.pdf')

    with open(base_path+'.pdf') as f:
        api.post('/path/data/smartclip/pdf', file=(slugify(clip.title)+'.pdf',f))

    if os.path.isfile(base_path+'.pdf'):
        os.remove(base_path+'.pdf')

    if os.path.isfile(base_path+'.html'):
        os.remove(base_path+'.html')
