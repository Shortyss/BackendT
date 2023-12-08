from datetime import date, datetime

from django.db import models
from django.db.models import Model, CharField, IntegerField, TextField, DateField, ForeignKey, DO_NOTHING, \
    ManyToManyField, SET_NULL, DateTimeField
from django.contrib.auth.models import User


# Create your models here.


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False)  # CharField => VARCHAR

    def __str__(self):
        return f"{self.name}"


class Person(Model):
    first_name = CharField(max_length=32, null=False, blank=False)
    last_name = CharField(max_length=32, null=False, blank=False)
    nationality = CharField(max_length=64, null=True, blank=True)
    birth_date = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def calculate_age(self):
        today = datetime.now().date()

        if self.date_of_death:
            # Pokud hercův úmrtí již nastalo, vypočtěme věk při úmrtí
            age_at_death = (self.date_of_death - self.birth_date).days // 365
            return age_at_death
        else:
            # Pokud hercův úmrtí nenastalo, vypočtěme aktuální věk
            age_now = (today - self.birth_date).days // 365
            return age_now

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Movie(Model):
    title_orig = CharField(max_length=64, null=False, blank=False)
    title_cz = CharField(max_length=64, null=True, blank=True)
    title_sk = CharField(max_length=64, null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    countries = ManyToManyField(Country, blank=True, related_name='movies_in_country')  # umožňuje jít oběma směry tabulek
    genres = ManyToManyField(Genre, blank=True, related_name='movies_of_genre')
    directors = ManyToManyField(Person, blank=False, related_name='directing_movie')
    actors = ManyToManyField(Person, blank=True, related_name='acting_in_movie')
    year = IntegerField(null=True, blank=True)
    video = CharField(max_length=128, null=True, blank=True)
    description = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        if self.title_cz:
            title_name = self.title_cz
        elif self.title_sk:
            title_name = self.title_sk
        else:
            title_name = self.title_orig

        if self.year is not None:
            title_name += f" ({self.year})"

        return title_name

    class Meta:
        ordering = ['title_orig']


class Rating(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.movie}: {self.rating} by {self.user}"


class Comment(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    comment = TextField(null=False, blank=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie}: {self.user} {self.comment[:20]}"


class Image(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    url = CharField(max_length=128, null=False, blank=False)
    description = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.movie}: {self.description}"
