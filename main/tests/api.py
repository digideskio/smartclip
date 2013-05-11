import json
from functools import partial

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tastypie.resources import ModelResource

from . import factories as f
from .testcase import SmartClipTestCase
from .. import api


class ResourceTestCase(SmartClipTestCase):
    def setUp(self):
        super(ResourceTestCase, self).setUp()
        self.api_name = 'v1'
        self.resource = ModelResource
        
    def resource_urls(self, resource_id=None, detail_uri_name='pk',
                      **kwargs):
        """
        Return a dictionary of named URLs included in Tastypie by default.
        These can be found in tastypie.resources.Resource.base_urls. They
        are included here as a convenience and a form of documentation.

        By using this method we can use reverse URL resolution and
        automatically have all of the kwargs needed by
        django.core.urlresolvers.reverse to return the URL string.

        """
        resource_name = self.resource._meta.resource_name
        return {
            'api_dispatch_list': {
                'resource_name': resource_name,
                'api_name': self.api_name
            },
            'api_get_schema': {
                'resource_name': resource_name,
                'api_name': self.api_name
            },
            'api_get_multiple': {
                'resource_name': resource_name,
                # 'resource_id' must be a semicolon-separated string of object
                # primary keys, e.g. '1;2;3;4'. Best way to get this would be
                # like so:

                # ids = Section.objects.all().values_list('id', flat=True)
                # ids = ';'.join(ids)

                # You'd then pass these in as the argument to resource_id.
                '%s_list' % detail_uri_name: resource_id,
                'api_name': self.api_name
            },
            'api_dispatch_detail': {
                'resource_name': resource_name,
                detail_uri_name: resource_id,
                'api_name': self.api_name
            }
        }
    
    
class ClippingTest(ResourceTestCase):
    def setUp(self):
        super(ClippingTest, self).setUp()
        self.resource = api.ClippingResource
        self.clipping = f.ClippingFactory(user=self.user)
        
    def test_get_detail(self):
        url_name = 'api_dispatch_detail'
        kwargs = self.resource_urls(self.clipping.id)[url_name]
        url = reverse(url_name, kwargs=kwargs)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

        self.client.login(username=self.user.username, password=self.pwd)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Create a new Clipping instance owned by a user other than self.user.
        # A GET for this resource should result in a 401.
        clip = f.ClippingFactory()
        user = clip.user
        user.set_password(self.pwd)
        user.save()

        kwargs = self.resource_urls(clip.id)[url_name]
        url = reverse(url_name, kwargs=kwargs)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)

        self.client.login(username=user.username, password=self.pwd)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        self.client.login(username=self.user.username, password=self.pwd)
        url_name = 'api_dispatch_list'
        kwargs = self.resource_urls()[url_name]
        url = reverse(url_name, kwargs=kwargs)
        payload = self._dumps(self._data())
        resp = self.client.post(url, data=payload,
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        content = json.loads(resp.content)
        self.assertIn('title', content.keys())
        
    def _data(self, **kwargs):
        data = {
            'html': '<b>Some HTML</b>',
            'title': 'My First Clipping!',
            'filename': 'my-first-clipping',
            'user': self.user
        }

        for k, v in kwargs.items():
            data[k] = v

        return data

    def _dumps(self, data):
        data = data.copy()
        url_name = 'api_dispatch_detail'
        kwargs = self.resource_urls(self.user.id)[url_name]
        data['user'] = reverse(url_name, kwargs=kwargs)
        return json.dumps(data)
        
