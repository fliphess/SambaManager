from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'app.views.auth.main', name='main'),
    url(r'^start/$', 'app.views.base.start', name='start'),

    url(r'^samba/?$', 'app.views.samba.index', name='samba'),

    url(r'^samba/list_users/$', 'app.views.samba.list_users', name='list_users'),
    url(r'^samba/list_groups/$', 'app.views.samba.list_groups', name='list_groups'),
    url(r'^samba/list_shares/$', 'app.views.samba.list_shares', name='list_shares'),

    url(r'^samba/add_user/$', 'app.views.samba.add_user', name='add_user'),
    url(r'^samba/edit_user/(?P<id>\d+)/$', 'app.views.samba.edit_user', name='edit_user'),
    url(r'^samba/delete_user/(?P<id>\d+)/$', 'app.views.samba.delete_user', name='delete_user'),

    url(r'^samba/add_group/$', 'app.views.samba.add_group', name='add_group'),
    url(r'^samba/delete_group/(?P<id>\d+)/$', 'app.views.samba.delete_group', name='delete_group'),

    url(r'^samba/add_share/$', 'app.views.samba.add_share', name='add_share'),
    url(r'^samba/edit_share/(?P<id>\d+)/$', 'app.views.samba.edit_share', name='edit_share'),
    url(r'^samba/delete_share/(?P<id>\d+)/$', 'app.views.samba.delete_share', name='delete_share'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'app.views.auth.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)