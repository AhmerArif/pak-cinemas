from django.contrib import admin
from .models import City, Cinema, Movie, Showtime

admin.site.register(City)
admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Showtime)
