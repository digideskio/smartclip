from .vagrant import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'scdb'
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher',
                    'django.contrib.auth.hashers.SHA1PasswordHasher']
