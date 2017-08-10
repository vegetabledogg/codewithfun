from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.learn, name='learn'),
    url(r'([a-z]+)/$', views.course_detail, name='course_detail'),
]