from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cards.views import *
from cards.views_xls2sql import convXls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'har.views.home', name='home'),
    # url(r'^har/', include('har.foo.urls')),
    url(r'^$', search),
    url(r'^all/$', show_all),
    url(r'^add/$', add_card),
    url(r'^search/?$', search),
    url(r'^xls2sql/$', convXls),
    url(r'^path/$', show_cur_path),
#    url(r'^admin_tools/',include('admin_tools.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
