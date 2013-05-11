from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from bs4 import BeautifulSoup
from main.tests.factories import UserFactory, ClippingFactory

class ViewsTests(TestCase):
    def setUp(self):
        super(ViewsTests, self).setUp()
        self.user = UserFactory()
        self.clipping = ClippingFactory(user=self.user)
        self.client = Client()

    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)        
        
    def test_view_clippings(self):
        self.client.login(username=self.user.username, password='testpassword')
        resp = self.client.get(reverse('view_clippings'))

        soup = BeautifulSoup(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(soup.findAll('li', {'class': 'clip_li'})), 1)

    def test_html_view(self):
        self.client.login(username=self.user.username, password='testpassword')
        resp = self.client.get(reverse('html_view'),
                               data={'clip_id': self.clipping.id})
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,
                         '<div class="test-class"><h1>Factory Test</h1></div>\n')

    def test_logout_user(self):
        logged_in = self.client.login(username=self.user.username,
                                      password='testpassword')
        
        self.assertTrue(logged_in)
        resp = self.client.get(reverse('logout_user'))
        self.assertEqual(resp.status_code, 200)

        soup = BeautifulSoup(resp.content)
        self.assertTrue(soup.findAll(text="You've been logged out."))
    
    def test_check_user(self):
        resp = self.client.get(reverse('check_user'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'no user')

        self.client.login(username=self.user.username, password='testpassword')
        resp = self.client.get(reverse('check_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'logged in')

