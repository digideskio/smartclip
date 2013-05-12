import os
from cStringIO import StringIO
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from wkhtmltopdf.utils import wkhtmltopdf
from django.contrib.auth import login
from django.contrib.auth.models import User

import smartfile
from smartclip import secrets
from smartclip import backends
from main.models import *


def generate_api(request):
    # "ACCESS_TOKEN" is inserted into the session in Smartfile.authenticate.
    token, secret = request.session.get('ACCESS_TOKEN', (None, None))
    return backends.Smartfile(client_token=secrets.OAUTH_TOKEN,
                              client_secret=secrets.OAUTH_SECRET,
                              access_token=token,
                              access_secret=secret)
    
def create_smartfile_docs(request, clip_id):
    clip = Clipping.objects.get(id=clip_id)
    base_path = settings.MEDIA_URL + clip.filename
    
    api = generate_api(request)
    create_smartfile_dirs(api)
    api.client.post('/path/data/smartclip/html',
                    file=(clip.filename+'.html',
                          StringIO(clip.html.encode('utf-8'))))
    
    html_file = open(base_path+'.html', 'w')
    html_file.write(clip.html.encode('ascii','xmlcharrefreplace'))
    html_file.close()

    wkhtmltopdf(pages=[base_path+'.html'], output=base_path+'.pdf')

    with open(base_path+'.pdf') as f:
        api.client.post('/path/data/smartclip/pdf',
                        file=(clip.filename+'.pdf',f))

    if os.path.isfile(base_path+'.pdf'):
        os.remove(base_path+'.pdf')

    if os.path.isfile(base_path+'.html'):
        os.remove(base_path+'.html')

def create_smartfile_dirs(api):
    for path in ['smartclip', 'smartclip.html', 'smartclip.pdf']:
        response = api.client.get('/path/info/%s' % path)
        if response.status_code >= 399:
            api.client.post('/path/oper/mkdir', path='/%s' % path)
    
def create_link(api, filename, **kwargs):
    message = kwargs.get('message', None)
    recipients = kwargs.get('recipients', None)
    name = kwargs.get('title', None)
    
    return api.client.post('/link', path='/smartclip/pdf/'+filename+'.pdf',
                           name=name, recipients=recipients, message=message,
                           read=True, list=True)
