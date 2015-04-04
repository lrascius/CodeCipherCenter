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
)
