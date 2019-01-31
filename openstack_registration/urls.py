from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.signup, name='signup'),
    url(r'^verify/$', views.verify, name='verify')
]