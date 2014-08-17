from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/?$', 'server_manager.views.command_overview', name='command_overview'),
    url(r'^command_editor/?$', 'server_manager.views.command_editor', name='command_editor'),
    url(r'^executor/(?P<name>\w+)/$', 'server_manager.views.command_executor', name='command_executor'),


    url(r'^add_command/$', 'server_manager.views.add_command', name='add_command'),
    url(r'^edit_command/(?P<name>\w+)/$', 'server_manager.views.edit_command', name='edit_command'),
    url(r'^delete_command/(?P<name>\w+)/$', 'server_manager.views.delete_command', name='delete_command'),
)
