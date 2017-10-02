from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.learn, name='learn'),
    url(r'^course/(?P<course_url>[0-9A-Za-z_\-$\+]+)/', include([
        url(r'^$', views.course_detail, name='course_detail'),
        url(r'^lesson/(?P<lesson_url>[0-9A-Za-z_\-$\+]+)/$', views.lesson, name='lesson'),
    ])),
]
