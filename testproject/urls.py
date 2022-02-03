from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'servicevis.views.home', name='home'),
    url(r'^services/', include('servicevis.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
