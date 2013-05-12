import random

from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

import factory
from taggit.models import Tag

from ..models import Clipping

User = get_user_model()

def _user_attributes():
    user_count = random.randint(1, 1000)
    attrs = {
        'username': 'testuser-%d' % user_count,
        'email': 'test%d@example.com' % user_count,
    }
    return attrs
    
class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = 'testuser'
    email = 'test@example.com'
    first_name = 'Test'
    last_name = 'User'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class ClippingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Clipping

    html = '<a href="http://google.com">Some HTML!</a>'
    title = 'Test Clipping'
    filename = 'test-clipping'
    source_url = 'http://google.com'
    text_only = False
    user = factory.SubFactory(UserFactory, **_user_attributes())
