from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pakcinemas.views.home', name='home'),
    # url(r'^pakcinemas/', include('pakcinemas.foo.urls')),
    url(r"^$", TemplateView.as_view(template_name="index.html")),
 
    url(r'^admin/', include(admin.site.urls)),
)
