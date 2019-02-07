from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.signup, name='signup'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^password_update/', views.password_update, name='password_update'),
]