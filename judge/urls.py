from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.learn, name='learn'),
    url(r'course1/', views.course1, name='course1'),
]