from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'control.views.auth.main', name='main'),
    url(r'^start/$', 'control.views.base.start', name='start'),
    url(r'^run_command/(?P<name>\w+)/$', 'control.views.base.run_command', name='run_command'),


    url(r'^samba_manager/', include('samba_manager.urls')),
    url(r'^server_manager/', include('server_manager.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'control.views.auth.logout_view', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)