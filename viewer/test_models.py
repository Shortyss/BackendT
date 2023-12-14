from django.db.models import Avg
from django.test import TestCase

from viewer.models import *


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title_orig="Test movie orig title",
            title_cz="Test movie title cz",
            title_sk="Test movie title sk",
            year=2023,
            video="",
            description="Popis filmu."
        )
        country_cz = Country.objects.create(name="CZ")
        country_sk = Country.objects.create(name="SK")
        movie.countries.add(country_cz)
        movie.countries.add(country_sk)
        genre_drama = Genre.objects.create(name="Drama")
        genre_comedy = Genre.objects.create(name="Komedie")
        movie.genres.add(genre_drama)
        movie.genres.add(genre_comedy)
        director1 = Person.objects.create(
            first_name="Jan",
            last_name="Juřička",
            birth_date=date.today(),
            biography="Biografie režiséra 1."
        )
        director2 = Person.objects.create(
            first_name="Martin",
            last_name="Malásek",
            birth_date=date.today(),
            biography="Biografie režiséra 2."
        )
        actor1 = Person.objects.create(
            first_name="David",
            last_name="Novák",
            birth_date=date.today(),
            biography="Biografie herce 1."
        )
        actor2 = Person.objects.create(
            first_name="Jana",
            last_name="Nováková",
            birth_date=date.today(),
            biography="Biografie herce 2."
        )
        movie.directors.add(director1)
        movie.directors.add(director2)
        movie.actors.add(actor1)
        movie.actors.add(actor2)
        movie.save()

    def test_title_orig(self):
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.title_orig, "Test movie orig title")

    def test_movie_str(self):
        movie = Movie.objects.get(title_orig="Test movie orig title")
        self.assertEqual(movie.__str__(), "Test movie title cz (2023)")

    def test_movie_actors(self):
        movie = Movie.objects.get(title_cz="Test movie title cz")
        number_of_actors = movie.actors.count()
        self.assertEqual(number_of_actors, 2)

    def test_movie_no_rating(self):
        movie = Movie.objects.get(id=1)
        number_of_ratings = Rating.objects.filter(movie=movie).count()
        self.assertEqual(number_of_ratings, 0)


class RatingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title_orig="Test movie orig title",
            title_cz="Test movie title cz",
            title_sk="Test movie title sk",
            year=2023,
            video="",
            description="Popis filmu."
        )
        country_cz = Country.objects.create(name="CZ")
        country_sk = Country.objects.create(name="SK")
        movie.countries.add(country_cz)
        movie.countries.add(country_sk)
        genre_drama = Genre.objects.create(name="Drama")
        genre_comedy = Genre.objects.create(name="Komedie")
        movie.genres.add(genre_drama)
        movie.genres.add(genre_comedy)
        director1 = Person.objects.create(
            first_name="Jan",
            last_name="Juřička",
            birth_date=date.today(),
            biography="Biografie režiséra 1."
        )
        director2 = Person.objects.create(
            first_name="Martin",
            last_name="Malásek",
            birth_date=date.today(),
            biography="Biografie režiséra 2."
        )
        actor1 = Person.objects.create(
            first_name="David",
            last_name="Novák",
            birth_date=date.today(),
            biography="Biografie herce 1."
        )
        actor2 = Person.objects.create(
            first_name="Jana",
            last_name="Nováková",
            birth_date=date.today(),
            biography="Biografie herce 2."
        )
        movie.directors.add(director1)
        movie.directors.add(director2)
        movie.actors.add(actor1)
        movie.actors.add(actor2)
        movie.save()

        user1 = User.objects.create(
            username="User1"
        )
        user2 = User.objects.create(
            username="User2"
        )
        Rating.objects.create(
            movie=movie,
            user=user1,
            rating=80
        )
        Rating.objects.create(
            movie=movie,
            user=user2,
            rating=90
        )

    def test_movie_rating_avg(self):
        movie = Movie.objects.get(id=1)
        avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
        self.assertEqual(avg_rating['rating__avg'], 85)

