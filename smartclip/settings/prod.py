from .base import *
from ..secrets import DB_PASSWORD

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scdb',
        'USER': 'sc_user',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'scinstance.c1mcwweis26q.us-east-1.rds.amazonaws.com',
        'PORT': 3306
    }}

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'smartclip.wsgi.application'

