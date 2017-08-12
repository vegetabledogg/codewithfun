from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.learn, name='learn'),
<<<<<<< HEAD
    url(r'^course/(?P<course_url>[\w]+)/$', views.course_detail, name='course_detail'),
    url(r'^course/(?P<course_url>[\w]+)/lesson/(?P<lesson_url>[\w]+)/(?P<lesson_num>[0-9]+)/$' , views.lesson, name='lesson'),

=======
    url(r'course/([\w]+)/$', views.course_detail, name='course_detail'),
    url(r'course/(?P<course_url>[\w]+)/lesson/(?P<lesson_url>[\w]+)/(?P<lesson_num>[0-9]+)/$' , views.lesson, name='lesson')
>>>>>>> 8af95fa3cb810391a7e7a1bc873fb938739a3300
]