from django.conf.urls import include, url
from django.contrib import admin
from . import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'codewithfun.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^learn/', include('judge.urls')),
]
