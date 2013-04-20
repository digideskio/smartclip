# Settings extension to support local development via the Vagrant box found at
# https://github.com/mattdeboard/smartclip-dev
from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '10.10.10.50'
    }
}

