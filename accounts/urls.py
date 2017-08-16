from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'edit/password/$', views.change_pwd, name='edit_pwd'),
    url(r'edit/learned_course/$', views.learned_course, name='learned_course'),
    url(r'^$', views.home, name='home'),
]
