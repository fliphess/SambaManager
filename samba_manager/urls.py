from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/?$', 'samba_manager.views.index', name='samba_manager'),

    url(r'^list_users/$', 'samba_manager.views.list_users', name='list_users'),
    url(r'^list_groups/$', 'samba_manager.views.list_groups', name='list_groups'),
    url(r'^list_shares/$', 'samba_manager.views.list_shares', name='list_shares'),

    url(r'^add_user/$', 'samba_manager.views.add_user', name='add_user'),
    url(r'^add_group/$', 'samba_manager.views.add_group', name='add_group'),
    url(r'^add_share/$', 'samba_manager.views.add_share', name='add_share'),

    url(r'^edit_user/(?P<id>\d+)/$', 'samba_manager.views.edit_user', name='edit_user'),
    url(r'^edit_share/(?P<id>\d+)/$', 'samba_manager.views.edit_share', name='edit_share'),

    url(r'^delete_user/(?P<id>\d+)/$', 'samba_manager.views.delete_user', name='delete_user'),
    url(r'^delete_group/(?P<id>\d+)/$', 'samba_manager.views.delete_group', name='delete_group'),
    url(r'^delete_share/(?P<id>\d+)/$', 'samba_manager.views.delete_share', name='delete_share'),
)