from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'SPLArch.core.views.home', name='home'),
    # url(r'^SPLArch/', include('SPLArch.foo.urls')),
	url(r'^imagem/$', 'SPLArch.core.views.pil_image'),
	url(r'pdf/$', 'SPLArch.core.views.pdf'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
