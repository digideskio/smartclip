from django.conf.urls import patterns, include, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^oauth-redirect/$', 'oauth_redirect', name='oauth_redirect'),
    url(r'^auth/$', 'authenticate', name='authenticate'),
    url(r'^login/$', 'verify_login', name='verify_login'),
    url(r'^feed/$', 'feed', name='feed')
)
