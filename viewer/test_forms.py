from django.test import TestCase

from viewer.models import *
from viewer.views import GenreModelForm, MovieForm


class GenreFormTest(TestCase):

    def test_genre_form_is_valid(self):
        form = GenreModelForm(data={'name': '  drama  '})
        # FIXME self.assertEqual(form.clean_name(), 'Drama')
        self.assertTrue(form.is_valid())


class MovieFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name='Česko')
        Country.objects.create(name='Slovensko')
        Genre.objects.create(name='Drama')
        Genre.objects.create(name='Komedie')
        Person.objects.create(
            first_name="Jan",
            last_name="Juřička",
            birth_date=date.today(),
            biography="Biografie režiséra 1."
        )
        Person.objects.create(
            first_name="Martin",
            last_name="Malásek",
            birth_date=date.today(),
            biography="Biografie režiséra 2."
        )
        Person.objects.create(
            first_name="David",
            last_name="Novák",
            birth_date=date.today(),
            biography="Biografie herce 1."
        )
        Person.objects.create(
            first_name="Jana",
            last_name="Nováková",
            birth_date=date.today(),
            biography="Biografie herce 2."
        )

    def test_movie_form_is_valid(self):
        form = MovieForm(data={
            'title_orig': 'New movie title orig',
            'title_cz': 'Nový film',
            'title_sk': '',
            'countries': ['1'],
            'genres': ['1', '2'],
            'directors': ['2'],
            'actors': ['3', '4'],
            'year': '2023',
            'video': '',
            'description': 'Popis'
        })
        self.assertTrue(form.is_valid())

    def test_movie_form_is_not_valid(self):
        form = MovieForm(data={
            'title_orig': '',
            'title_cz': 'Nový film',
            'title_sk': '',
            'countries': ['1'],
            'genres': ['1', '2'],
            'directors': ['2'],
            'actors': ['3', '4'],
            'year': '2023',
            'video': '',
            'description': 'Popis'
        })
        self.assertFalse(form.is_valid())


# TODO: PersonFormTest