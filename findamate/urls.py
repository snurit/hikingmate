from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^hike/$', views.hike, name='hike'),
    url(r'^hike/(?P<hike_id>[0-9]+)?/$', views.hike, name='hike'),
]
