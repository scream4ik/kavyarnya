from django.conf.urls import patterns, url

from views import *


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^profile/edit/$', ProfileEditView.as_view(), name='profile_edit'),
)
