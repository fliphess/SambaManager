from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'samba_manager.views.auth.main', name='main'),
    url(r'^start/$', 'samba_manager.views.base.start', name='start'),

    url(r'^samba_manager/?$', 'samba_manager.views.samba.index', name='samba_manager'),

    url(r'^samba_manager/list_users/$', 'samba_manager.views.samba.list_users', name='list_users'),
    url(r'^samba_manager/list_groups/$', 'samba_manager.views.samba.list_groups', name='list_groups'),
    url(r'^samba_manager/list_shares/$', 'samba_manager.views.samba.list_shares', name='list_shares'),

    url(r'^samba_manager/add_user/$', 'samba_manager.views.samba.add_user', name='add_user'),
    url(r'^samba_manager/edit_user/(?P<id>\d+)/$', 'samba_manager.views.samba.edit_user', name='edit_user'),
    url(r'^samba_manager/delete_user/(?P<id>\d+)/$', 'samba_manager.views.samba.delete_user', name='delete_user'),

    url(r'^samba_manager/add_group/$', 'samba_manager.views.samba.add_group', name='add_group'),
    url(r'^samba_manager/delete_group/(?P<id>\d+)/$', 'samba_manager.views.samba.delete_group', name='delete_group'),

    url(r'^samba_manager/add_share/$', 'samba_manager.views.samba.add_share', name='add_share'),
    url(r'^samba_manager/edit_share/(?P<id>\d+)/$', 'samba_manager.views.samba.edit_share', name='edit_share'),
    url(r'^samba_manager/delete_share/(?P<id>\d+)/$', 'samba_manager.views.samba.delete_share', name='delete_share'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'samba_manager.views.auth.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)