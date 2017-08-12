from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.learn, name='learn'),
    url(r'^course/(?P<course_url>[\w]+)/$', views.course_detail, name='course_detail'),
    url(r'^course/(?P<course_url>[\w]+)/lesson/(?P<lesson_url>[\w]+)/(?P<lesson_num>[0-9]+)/$' , views.lesson, name='lesson'),

]