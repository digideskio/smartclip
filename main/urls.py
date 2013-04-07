from django.conf.urls import patterns, include, url

urlpatterns = patterns('smartclip.main.views',
    url(r'^$', 'home', name='home'),
    url(r'^oauth-redirect/$', 'oauth_redirect', name='oauth_redirect'),
    url(r'^auth/$', 'authenticate', name='authenticate'),
    url(r'^login/$', 'login', name='login')
)
