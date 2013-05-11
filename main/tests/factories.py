import factory

from django.contrib.auth.models import User

from main.models import Clipping


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'
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

    html = '<div class="test-class"><h1>Factory Test</h1></div>'
    title = 'Test Clipping'
    filename = 'test-clipping'
    user = factory.SubFactory(UserFactory)
