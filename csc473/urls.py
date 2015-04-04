from django.conf.urls import patterns, include, url
from django.contrib import admin
from cccenter import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'csc473.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name="cccenter"),
    url(r'^register$', views.register, name="cccenter"),   
    url(r'^cccenter/', include('cccenter.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # User authentication urls
    url(r'^accounts/login/$', 'cccenter.views.login'),
	url(r'^accounts/auth/$', 'cccenter.views.auth_view'),
	url(r'^accounts/logout/$', 'cccenter.views.logout'),
	url(r'^accounts/loggedin/$', 'cccenter.views.loggedin'),
	url(r'^accounts/invalid/$', 'cccenter.views.invalid_login'),
)
