from django.conf.urls import patterns, include, url

urlpatterns = patterns('smartclip.main.views',
    url(r'^$', 'home', name='home'),
    url(r'^oauth-redirect/$', 'oauth_redirect', name='oauth_redirect'),
    url(r'^clippings/$', 'view_clippings', name='view_clippings'),
    url(r'^auth/$', 'authenticate', name='authenticate'),
)
