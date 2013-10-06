from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings

# from cinema_movies.views import movie_list, movie_detail

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pakcinemas.views.home', name='home'),
    # url(r'^pakcinemas/', include('pakcinemas.foo.urls')),
    url(r"^$", TemplateView.as_view(template_name="index.html")),
    # url(r"^movies/", include("cinema_movies.urls", namespace = "movie")),
	url(r'^admin/', include(admin.site.urls)),
    url(r"^movies/", include("cinema_movies.urls", namespace="movie")),
)

# TODO: Throw this garbage out when deploying to S3 later
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
 )

urlpatterns += patterns('',
	(r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)