from django.db import models
from autoslug import AutoSlugField
from pytz import timezone
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField

class City(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	name = models.CharField(max_length=255, unique=True)
	long_name = models.CharField(max_length=255, unique=True)
	slug = AutoSlugField(populate_from='name')

	def __unicode__(self):
		return self.name

class Cinema(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True,editable=False)
	name = models.CharField(max_length=255, db_index=True, unique=True)
	slug = AutoSlugField(populate_from='name')
	website_url = models.URLField()
	city = models.ForeignKey(City, db_index=True, related_name="cinemas") 

	def __unicode__(self):
		return self.name

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

	@models.permalink
	def get_absolute_url(self):
		return ("movie:detail", (), {"slug": self.slug})

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
		# but it's sad.
		return self.movie.name + ": " + self.showing_at.astimezone(timezone(settings.TIME_ZONE)).strftime('%l:%M%p %Z on %b %d, %Y') + " at " + self.cinema.name
