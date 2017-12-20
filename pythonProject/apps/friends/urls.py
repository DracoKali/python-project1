from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^profile$', views.profile),
    url(r'^info/(?P<id>\d+)$', views.friendInfo),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^remove/(?P<id>\d+)$', views.remove)
    
]
