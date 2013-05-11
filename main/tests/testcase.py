from django.test import TestCase

from .factories import UserFactory


class SmartclipTestCase(TestCase):
    def setUp(self):
        super(SmartclipTestCase, self).setUp()
        self.pwd = 'password'
        self.user = UserFactory.build()
        self.user.set_password(self.pwd)
        self.user.save()
