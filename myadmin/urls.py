from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^judge/lesson/add/$', views.add_lesson, name='add_lesson'),
    url(r'^judge/lesson/(?P<lesson_id>[0-9]+)/delete/$', views.delete_lesson, name='delete_lesson'),
]
