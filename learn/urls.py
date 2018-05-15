from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.learn, name='learn'),
    url(r'^category', views.learn, name='learn_by_categories'),
    url(r'^course', views.course_detail, name='course_detail'),
    url(r'^lesson', views.lesson, name='lesson'),
]
