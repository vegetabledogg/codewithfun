from django.conf.urls import include, url
from django.contrib import admin
from . import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'codewithfun.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': './avatar'}),
    url(r'^admin/', include('myadmin.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^learn/', include('judge.urls')),
]
