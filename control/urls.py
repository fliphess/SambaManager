from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from control.views.base import IndexPage

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', login_required(IndexPage.as_view()), name='main'),
    url(r'^start/$', login_required(IndexPage.as_view()), name='start'),

    url(r'^samba_manager/', include('samba_manager.urls')),
    url(r'^server_manager/', include('server_manager.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'control.views.auth.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
