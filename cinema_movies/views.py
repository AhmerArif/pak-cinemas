from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import City, Cinema, Movie, Showtime

class MovieListView(ListView):
	model = Movie

	def get_queryset(self):
		queryset = super(MovieListView,self).get_queryset()
		return queryset

class MovieDetailView(DetailView):
	model = Movie

	def get_queryset(self):
		queryset = super(MovieDetailView,self).get_queryset()
		return queryset