from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('core.urls')),
    url(r'', include('stats.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)

# Do not forget to serve static files in production with something but django
if settings.DEBUG and settings.MEDIA_URL.startswith('/'):

    urlpatterns += patterns('',

        url(r'^%s/(?P<path>.*)$' % settings.STATIC_URL.strip('/'),
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT,
             'show_indexes': True}),
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
             'show_indexes': True}),
    )
