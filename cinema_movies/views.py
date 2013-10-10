from django.views.generic import ListView, DetailView
from django.utils import simplejson
from django.http import *
from django.core import serializers

from .models import City, Cinema, Movie, Showtime

# class AJAXListMixin(object):

# 	def dispatch(self, request, *args, **kwargs):
# 		if request.is_ajax():
# 			return super(AJAXListMixin, self).dispatch(request, *args, **kwargs)
# 		super(AJAXListMixin, self).dispatch(request,*args, **kwargs)

# 	def get_queryset(self):
# 		return (
# 			super(AJAXListMixin, self)
# 			.get_queryset()
# 			.filter(ajaxy_param=self.request.GET.get('client_response'))
# 		)

# 	def get(self, request, *args, **kwargs):
# 		return HttpResponse(serializers.serialize('json', self.get_queryset()))


class MovieListView(ListView):
	model = Movie

	def get_queryset(self):
		queryset = City.objects.current_city(self.request.GET.get('city_slug', 'All')).available_movies()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(MovieListView, self).get_context_data(**kwargs)
		context['city_list'] = City.objects.all().order_by('name')
		City.objects.current_city(self.request.GET.get('city_slug', 'All'))
		return context

	def render_to_response(self, context, **response_kwargs):
		if self.request.is_ajax():
			return HttpResponse(simplejson.dumps(City.objects.current_city(self.request.GET.get('client_response', 'All')).available_movies()), mimetype='application/javascript')
		return super(MovieListView,self).render_to_response(context, **response_kwargs)

	# def get_template_names(self):
	# 	if self.request.is_ajax():
	# 		return HttpResponse(simplejson.dumps("success"), mimetype="application/json")
	# 	else:
	# 		return ['cinema_movies/movie_list.html']

class MovieDetailView(DetailView):
	model = Movie

	def get_queryset(self):
		queryset = super(MovieDetailView,self).get_queryset()
		return queryset