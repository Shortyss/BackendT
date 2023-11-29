from django.db import models
from django.db.models import Model, CharField, IntegerField, TextField, DateField, ForeignKey, DO_NOTHING, \
    ManyToManyField, SET_NULL
from django.contrib.auth.models import User

# Create your models here.


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Countries"


class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False)  # CharField => VARCHAR

    def __str__(self):
        return f"{self.name}"


class Person(Model):
    first_name = CharField(max_length=32, null=False, blank=False)
    last_name = CharField(max_length=32, null=False, blank=False)
    birth_date = DateField()
    biography = TextField



class Movie(Model):
    title_orig = CharField(max_length=64, null=False, blank=False)
    title_cz = CharField(max_length=64)
    title_sk = CharField(max_length=64)
    countries = ManyToManyField(Country, blank=True, related_name='movies_in_country')  # umožňuje jít oběma směry tabulek
    genres = ManyToManyField(Genre, blank=True, related_name='movies_of_genre')
    directors = ManyToManyField(Person, blank=False, related_name='directing_movie')
    actors = ManyToManyField(Person, blank=True, related_name='acting_in_movie')
    year = IntegerField()
    video = CharField(max_length=128)
    description = TextField()   # TextField je dobrý pro dlouhé psaní


class Rating(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = IntegerField(null=False, blank=False)


class Comment(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    comment = TextField(null=False, blank=False)


class Image(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    url = CharField(max_length=128, null=False, blank=False)
    description = TextField
