import factory

from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = 'testuser'
    email = 'test@example.com'
    first_name = 'Test'
    last_name = 'User'

