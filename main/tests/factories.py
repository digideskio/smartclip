import random

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import factory
from taggit.models import Tag

from ..models import Clipping


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


class TagFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Tag

    name = 'Test Tag'
    slug = 'test-tag'
    

class ClippingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Clipping

    html = '<a href="http://google.com">Some HTML!</a>'
    title = 'Test Clipping'
    filename = 'test-clipping'
    source_url = 'http://google.com'
    text_only = False
    user = factory.SubFactory(UserFactory, **_user_attributes())

