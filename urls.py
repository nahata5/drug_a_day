from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('drugs.urls'), name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^drugs/', include('drugs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
