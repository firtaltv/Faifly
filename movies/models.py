from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class MovieImage(models.Model):
    image = models.ImageField()


class MovieSeries(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Movie Series'


class Movie(models.Model):
    name = models.CharField(max_length=50, unique=True)
    genre = models.ManyToManyField(Genre, related_name='genres')
    image = models.ImageField(null=True, blank=True)
    url = models.SlugField(max_length=65, unique=True)
    series = models.ForeignKey(MovieSeries, on_delete=models.CASCADE)
    voters = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies/.html')


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField('Comment ', max_length=300)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Vote(models.Model):
    value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(value__range=(0, 5)), name='valid_value'),
            UniqueConstraint(fields=['user', 'movie'], name='rating_once')
        ]

    def __str__(self):
        return str(self.value)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    watch_later = models.ManyToManyField(Movie, related_name='later')
    viewed = models.ManyToManyField(Movie, related_name='viewed')
    abandoned = models.ManyToManyField(Movie, related_name='abandoned')
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
