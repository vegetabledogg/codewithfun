from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'codewithfun.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/judge/lesson/add/$', 'codewithfun.views.add_lesson', name='add_lesson'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^learn/', include('judge.urls')),
]
