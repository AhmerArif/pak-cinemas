from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings

from cinema_movies.views import MovieListView, MovieDetailView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pakcinemas.views.home', name='home'),
    # url(r'^pakcinemas/', include('pakcinemas.foo.urls')),
    # url(r"^movies/", include("cinema_movies.urls", namespace = "movie")),
	url(r'^admin/', include(admin.site.urls)),
    # url(r"^movies/", include("cinema_movies.urls", namespace="movie")),
    url(r"^$", MovieListView.as_view(), name="list"),
    url(r'^city/(?P<city_slug>[\w-]+)/movies/(?P<slug>[\w-]+)/$', MovieDetailView.as_view(), name="detail"),
    url(r"^city/(?P<city_slug>[\w-]+)", MovieListView.as_view(), name="list"),
    # url(r"^(P<city-slug>[\w-]+)/(?P<movie-slug>[\w-]+)/$", MovieDetailView.as_view(), name="detail"),
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