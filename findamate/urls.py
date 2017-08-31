from django.conf.urls import url, include
from findamate import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^hike/$', views.hike, name='hike'),
    url(r'^hike/(?P<hike_id>[0-9]+)?/$', views.hike, name='hike'),
    url(r'^path/$', views.path, name='path'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^api/hiker/$', views.api_user),
    url(r'^api/hiker/(?P<pk>[0-9]+)/$', views.api_user_detail),
    url(r'^api/hike/$', views.api_hike),
    url(r'^api/hike/(?P<pk>[0-9]+)/$', views.api_hike_detail),
    url(r'^api/enrollment/$', views.api_enrollment),
    url(r'^api/enrollment/(?P<pk>[0-9]+)/$', views.api_enrollment_detail),
]
