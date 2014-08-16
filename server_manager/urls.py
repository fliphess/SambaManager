from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/?$', 'server_manager.views.overview', name='command_overview'),
    url(r'^list_commands/?$', 'server_manager.views.list_commands', name='list_commands'),

    url(r'^add_command/$', 'server_manager.views.add_command', name='add_command'),
    url(r'^edit_command/(?P<name>\w+)/$', 'server_manager.views.edit_command', name='edit_command'),
    url(r'^delete_command/(?P<name>\w+)/$', 'server_manager.views.delete_command', name='delete_command'),
)
