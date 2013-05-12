import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test.client import Client

from bs4 import BeautifulSoup
from mock import patch

from .factories import ClippingFactory, UserFactory
from .testcase import SmartClipTestCase
from .. import views
from ..models import Clipping


def dummy_smartfile_docs(request, clip_id):
    return None

def dummy_authenticate(request):
    return UserFactory(username='test-dummy')

def get_pdf(*args, **kwargs):
    with open('/'.join([settings.PATH, 'main/tests/test.pdf'])) as f:
        return HttpResponse(f)

def share_valid_form(*args, **kwargs):
    return HttpResponse('{"href": "https://file.ex/example-clip-link/"}')

def share_invalid_form(*args, **kwargs):
    return HttpResponse('{"field_errors": {"path": ["Path test.pdf does not exist."]}}')

def empty_return(*args, **kwargs):
    return None

    
class ViewsTests(SmartClipTestCase):
    def setUp(self):
        super(ViewsTests, self).setUp()
        self.clipping = ClippingFactory(user=self.user)
        self.client = Client()

    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_authenticate(self):
        with patch('smartclip.backends.Smartfile') as m:
            api = m.return_value
            api.authenticate = dummy_authenticate

            resp = self.client.get(reverse('authenticate'))
            self.assertEqual(resp.status_code, 302)
            
    def test_view_clippings(self):
        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(reverse('view_clippings'))

        soup = BeautifulSoup(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(soup.findAll('li', {'class': 'clip_li'})), 1)

    def test_html_view(self):
        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(reverse('html_view'),
                               data={'clip_id': self.clipping.id})
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.strip(), self.clipping.html.strip())


    @patch('main.auth.create_smartfile_docs', new=dummy_smartfile_docs)
    def test_render_documents(self):
        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(reverse('render_documents'),
                               data={'clip_id': self.clipping.id})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'rendered documents')

    def test_sort_clips(self):
        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(reverse('sort_clips'),
                               data={'sort_key': 'title'})
        self.assertEqual(resp.status_code, 200)
        
    def test_pdf_view(self):
        self.client.login(username=self.user.username, password=self.pwd)
        url = reverse(views.pdf_view)

        with patch('smartclip.backends.smartfile_backend.SmartfileClient') as m:
            client = m.return_value
            client.get = get_pdf
            resp = self.client.get(url, {'clip_id': self.clipping.id})
            self.assertEqual(resp.status_code, 200)

    def test_logout_user(self):
        logged_in = self.client.login(username=self.user.username,
                                      password=self.pwd)
        
        self.assertTrue(logged_in)
        resp = self.client.get(reverse('logout_user'))
        self.assertEqual(resp.status_code, 200)

        soup = BeautifulSoup(resp.content)
        self.assertTrue(soup.findAll(text="You've been logged out."))
    
    def test_check_user(self):
        resp = self.client.get(reverse('check_user'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'no user')

        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(reverse('check_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'logged in')

    def test_delete_clipping(self):
        self.client.login(username=self.user.username, password=self.pwd)


        with patch('smartclip.backends.smartfile_backend.SmartfileClient') as m:
            client = m.return_value
            client.post = empty_return

            someone_elses_clip = ClippingFactory()
            resp = self.client.get(reverse('delete_clipping',
                                           kwargs={'clip_id': someone_elses_clip.id}))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content, 'not authorized')
            
            clip_to_delete = ClippingFactory(user=self.user)
            resp = self.client.get(reverse('delete_clipping',
                                           kwargs={'clip_id': clip_to_delete.id}))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content, 'deleted')
            with self.assertRaises(Clipping.DoesNotExist):
                Clipping.objects.get(id=clip_to_delete.id)
            
    def test_get_share_form(self):
        self.client.login(username=self.user.username, password=self.pwd)
        someone_elses_clip = ClippingFactory()
        resp = self.client.get(reverse('share_form',
                                       kwargs={'clip_id': someone_elses_clip.id}))
        self.assertEqual(resp.content, 'not authorized')

        resp = self.client.get(reverse('share_form',
                                       kwargs={'clip_id': self.clipping.id}))
        self.assertEqual(resp.status_code, 200)

    def test_post_share_form(self):
        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.post(reverse('share_form',
                                        kwargs={'clip_id': self.clipping.id}))
        self.assertEqual(resp.status_code, 200)
        soup = BeautifulSoup(resp.content)
        self.assertTrue(soup.find('form'))

        with patch('smartclip.backends.smartfile_backend.SmartfileClient') as m:
            client = m.return_value
            client.post = share_valid_form
            
            resp = self.client.post(reverse('share_form',
                                            kwargs={'clip_id': self.clipping.id}),
                                            data={'title': 'Test Title',
                                                  'message': 'Test message',
                                                  'recipients': 'a@foo.com, b@foo.com'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content, 'success')
            
            client.post = share_invalid_form
            resp = self.client.post(reverse('share_form',
                                            kwargs={'clip_id': self.clipping.id}),
                                            data={'title': 'Test Title',
                                                  'message': 'Test message',
                                                  'recipients': 'a@foo.com, b@foo.com'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content, 'failure')
