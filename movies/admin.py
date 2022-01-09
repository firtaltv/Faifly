from django.contrib import admin
from .models import *

admin.site.register(Profile)


@admin.register(Movie)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name', )}


@admin.register(MovieSeries, Genre)
class MovieSeriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Review, Vote)
class ReviewMovieAdmin(admin.ModelAdmin):
    pass
