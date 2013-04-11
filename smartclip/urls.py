from django.conf.urls import patterns, include, url
from tastypie.api import Api
from main.api import ClippingResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ClippingResource())

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^oauth-redirect/$', 'oauth_redirect', name='oauth_redirect'),
    url(r'^auth/$', 'authenticate', name='authenticate'),
    url(r'^login/$', 'verify_login', name='verify_login'),
    url(r'^logout/$', 'logout_user', name='logout_user'),
    url(r'^feed/$', 'feed', name='feed'),
    url(r'^ext/user/$', 'check_user', name='check_user'),
    (r'^api/', include(v1_api.urls))
    )
