from django.conf.urls import url, include
from findamate import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^hike/$', views.hike, name='hike'),
    url(r'^hike/(?P<hike_id>[0-9]+)?/$', views.hike, name='hike'),
    url(r'^path/$', views.path, name='path'),
    url(r'^signup/$', views.signup, name='signup'),
]
