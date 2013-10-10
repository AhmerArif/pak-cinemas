from django.db import models
from autoslug import AutoSlugField
from pytz import timezone as timezone_object 
from django.conf import settings
from django.utils import timezone
import datetime
from easy_thumbnails.fields import ThumbnailerImageField

class CityManager(models.Manager):
	def current_city(self, city_slug=""):
		city = City.objects.filter(slug__iexact=city_slug)
		# print city
		return city[0] if city else City.objects.filter(name__exact="All")[0]

class City(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	name = models.CharField(max_length=255, unique=True)
	long_name = models.CharField(max_length=255, unique=True)
	slug = AutoSlugField(populate_from='name')
	objects = CityManager()

	def __unicode__(self):
		return self.name

	def available_cinemas_for_movie(self, movie_name="", future_date =7):
		if self.name == "All":
			cinemas = Cinema.objects.all()
		else:
			cinemas = self.cinemas.all()

		return cinemas.filter(showtimes__movie__name__exact=movie_name, 
			showtimes__showing_at__gte=(timezone.now() - datetime.timedelta(hours=2)),
			showtimes__showing_at__lte=(timezone.now() + datetime.timedelta(days=future_date))
			).order_by('name')

	def available_movies(self, future_date=7):
		if self.name == "All":
			cinemas = Cinema.objects.all()
		else:
			cinemas = self.cinemas.all()

		return Movie.objects.filter(showtimes__cinema__id__in=cinemas,
			showtimes__showing_at__gte=(timezone.now() - datetime.timedelta(hours=12)), #change me back to 2
			showtimes__showing_at__lte=(timezone.now() + datetime.timedelta(days=future_date))
			).order_by('name')


	# @models.permalink
	# def get_absolute_url(self):
	# 	return ("city:detail", (), {"slug": self.slug})


class Movie(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	name = models.CharField(max_length=255, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name')
	imdb_url = models.URLField(blank=True)
	rotten_tomatoes_url = models.URLField(blank=True)
	movie_poster = ThumbnailerImageField(upload_to='images/', default = 'images/no-img.jpg')
	# movie_poster = models.ImageField(upload_to = 'images/', default = 'images/no-img.jpg')
	# thumb_url = get_thumbnailer(movie_poster)['small'].url

	def __unicode__(self):
		return self.name

	# @models.permalink
	# def get_absolute_url(self):
	# 	return ("movie:detail", (), {"slug": self.slug})

	def current_showtimes(self, future_date=7):
		showtimes = self.showtimes.filter(showing_at__gte=(timezone.now() - datetime.timedelta(hours=2)))
		return showtimes.filter(showing_at__lte=(timezone.now() + datetime.timedelta(days=future_date))) 
		# return self.showtimes.all()


class Cinema(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	name = models.CharField(max_length=255, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name')
	website_url = models.URLField()
	city = models.ForeignKey(City, db_index=True, related_name="cinemas")
	movies = models.ManyToManyField(Movie, through='Showtime')

	def current_showtimes_for_movie(self, movie_name="",future_date=7):
		return self.showtimes.filter(movie__name=movie_name,
			showing_at__gte=(timezone.now() - datetime.timedelta(hours=2)),
			showing_at__lte=(timezone.now() + datetime.timedelta(days=future_date))
			).order_by('showing_at') 

	def __unicode__(self):
		return self.name

# Maps the details of the many to many relationship between movies and cinemas 
class Showtime(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	movie = models.ForeignKey(Movie, related_name="showtimes")
	cinema = models.ForeignKey(Cinema, related_name="showtimes")
	showing_at = models.DateTimeField()
	show_3d_or_2d = models.CharField(max_length=3, choices=(('2D','2-D'),('3D', '3-D')), default='2D')
	show_adults_only = models.BooleanField(default=False) 

	def __unicode__(self):
		# Converts the UTC time from the DB to the application timezone. Can't see a better way to do this in Django currently
		return self.movie.name + ": " + self.showing_at.astimezone(timezone_object(settings.TIME_ZONE)).strftime('%l:%M%p %Z on %b %d, %Y') + " at " + self.cinema.name

