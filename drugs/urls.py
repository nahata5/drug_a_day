from django.conf.urls import patterns, url
from drugs import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)