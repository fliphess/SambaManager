from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/?$', 'server_control.views.index', name='server_control'),

    url(r'^overview/$', 'server_control.views.overview', name='control_overview'),
    url(r'^list_commands/$', 'server_control.views.list_commands', name='list_commands'),


    url(r'^add_command/$', 'server_control.views.add_command', name='add_command'),
    url(r'^edit_command/(?P<name>\w+)/$', 'server_control.views.edit_command', name='edit_command'),
    url(r'^delete_command/(?P<name>\w+)/$', 'server_control.views.delete_command', name='delete_command'),
)
