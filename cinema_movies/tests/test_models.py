from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase
from model_mommy import mommy
from pytz import timezone
import datetime
from django.utils import timezone
from ..models import City, Cinema, Movie, Showtime


class CityTests(TestCase):

    def test_model_creation(self):
        city = mommy.make('City')
        self.assertTrue(isinstance(city, City))
        self.assertEqual(city.__unicode__(), city.name)

    def test_available_cinemas_for_movie_cinema_correct_city(self):
        city = mommy.make('City')
        cinema = mommy.make('Cinema')
        movie = mommy.make('Movie')
        showtime = mommy.make('Showtime',cinema=cinema, movie=movie)
        self.assertNotIn(cinema, city.available_cinemas_for_movie(movie.name))
        cinema.city = city
        cinema.save()
        self.assertIn(cinema, city.available_cinemas_for_movie(movie.name))

    def test_available_cinemas_for_movie_cinema_correct_movie(self):
        city = mommy.make('City')
        cinema = mommy.make('Cinema', city=city)
        movie = mommy.make('Movie')
        showtime = mommy.make('Showtime', movie=movie)
        self.assertNotIn(cinema, city.available_cinemas_for_movie(movie.name))
        showtime.cinema = cinema 
        showtime.save()
        self.assertIn(cinema, city.available_cinemas_for_movie(movie.name))

    def test_available_cinemas_for_movie_cinema_correct_time(self):
        city = mommy.make('City')
        cinema = mommy.make('Cinema', city=city)
        movie = mommy.make('Movie')
        showtime = mommy.make('Showtime', movie=movie, cinema=cinema, showing_at=(timezone.now() + datetime.timedelta(days=60)))
        self.assertNotIn(cinema, city.available_cinemas_for_movie(movie.name))
        showtime.showing_at = timezone.now() - datetime.timedelta(days=2)
        showtime.save()     
        self.assertNotIn(cinema, city.available_cinemas_for_movie(movie.name))
        showtime.showing_at = timezone.now()  
        showtime.save()
        self.assertIn(cinema, city.available_cinemas_for_movie(movie.name))

class MovieTests(TestCase):

    def test_model_creation(self):
        movie = mommy.make('Movie')
        self.assertTrue(isinstance(movie, Movie))
        self.assertEqual(movie.__unicode__(), movie.name)
        self.assertNotEqual(movie.slug, slugify(movie.name))
        movie.slug = slugify(movie.name)
        self.assertEqual(movie.slug, slugify(movie.name))

    def test_movie_all_showtimes(self):
        movie = mommy.make('Movie')
        showtime_good = mommy.make('Showtime',movie=movie)
        showtime_bad = mommy.make('Showtime')
        self.assertIn(showtime_good, movie.showtimes.all())
        self.assertNotIn(showtime_bad, movie.showtimes.all())

    def test_movie_current_showtimes(self):
        movie = mommy.make('Movie')
        latest_showtimes = mommy.make('Showtime',movie=movie, _quantity=2)
        self.assertIn(latest_showtimes[0], movie.current_showtimes())
        self.assertIn(latest_showtimes[1], movie.current_showtimes())

    def test_movie_old_showtimes(self):
        movie = mommy.make('Movie')
        old_showtimes = mommy.make('Showtime',movie=movie, showing_at=(timezone.now() - datetime.timedelta(days=1)), _quantity=2)
        self.assertNotIn(old_showtimes[0], movie.current_showtimes())
        self.assertNotIn(old_showtimes[1], movie.current_showtimes())

    def test_movie_future_showtimes(self):
        movie = mommy.make('Movie')
        future_showtimes = mommy.make('Showtime',movie=movie, showing_at=(timezone.now() + datetime.timedelta(days=60)), _quantity=2)
        self.assertNotIn(future_showtimes[0], movie.current_showtimes())
        self.assertNotIn(future_showtimes[1], movie.current_showtimes())


    # def test_model_url(self):
        # movie = self.create_city()
        # self.assertEqual(movie.get_absolute_url(),
            # reverse('movie:detail', kwargs={'slug': movie.slug}))

