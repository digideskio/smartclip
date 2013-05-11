from django.test import TestCase

from .factories import UserFactory


class SmartClipTestCase(TestCase):
    def setUp(self):
        super(SmartClipTestCase, self).setUp()
        self.pwd = 'password'
        self.user = UserFactory(password=self.pwd)
