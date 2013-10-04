from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r"^$", views.MovieListView.as_view(), name="list"),
	url(r"^(?P<slug>[\w-]+)", views.MovieDetailView.as_view(), name="detail"),
	# url(r"^$", views.MovieListView.as_view(), name="list"),
)
