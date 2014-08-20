from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from samba_manager.views import IndexView, ListUsers, ListShares, ListGroups, AddGroup, AddUser, AddShare, EditUser, \
    EditShare, DeleteShare, DeleteGroup, DeleteUser

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/?$', login_required(IndexView.as_view()), name='samba_manager'),

    url(r'^list_users/$', login_required(ListUsers.as_view()), name='list_users'),
    url(r'^list_groups/$', login_required(ListGroups.as_view()), name='list_groups'),
    url(r'^list_shares/$', login_required(ListShares.as_view()), name='list_shares'),

    url(r'^add_user/$', login_required(AddUser.as_view()), name='add_user'),
    url(r'^add_group/$', login_required(AddGroup.as_view()), name='add_group'),
    url(r'^add_share/$', login_required(AddShare.as_view()), name='add_share'),

    url(r'^edit_user/(?P<id>\d+)/$', login_required(EditUser.as_view()), name='edit_user'),
    url(r'^edit_share/(?P<id>\d+)/$', login_required(EditShare.as_view()), name='edit_share'),

    url(r'^delete_user/(?P<id>\d+)/$', login_required(DeleteUser.as_view()), name='delete_user'),
    url(r'^delete_group/(?P<id>\d+)/$', login_required(DeleteGroup.as_view()), name='delete_group'),
    url(r'^delete_share/(?P<id>\d+)/$', login_required(DeleteShare.as_view()), name='delete_share'),
)