from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^server_control/?$', 'server_control.views.index', name='server_control'),
)