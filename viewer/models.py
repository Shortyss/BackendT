from django.db import models
from django.db.models import Model, CharField, IntegerField, TextField, DateField, ForeignKey, DO_NOTHING


# Create your models here.


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False)


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
    # TODO: countries
    # TODO: genres
    # TODO: directors
    # TODO: actors
    year = IntegerField()
    # TODO: ratings
    # TODO: comments
    # TODO: images
    video = CharField(max_length=128)
    description = TextField()   # TextField je dobrý pro dlouhé psaní


class Rating(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    # TODO: user
    rating = IntegerField(null=False, blank=False)


class Comment(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    # TODO: user
    comment = TextField(null=False, blank=False)


class Image(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    url = CharField(max_length=128, null=False, blank=False)
    description = TextField
