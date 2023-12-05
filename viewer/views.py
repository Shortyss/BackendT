from django.http import HttpResponse
from django.shortcuts import render

from viewer.models import *


# Create your views here.


def hello(request):
    return HttpResponse("Hello World!")


def hello2(request, s):
    return HttpResponse(f"Hello, {s} world!")


def hello3(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Hello, {s} world!")


def hello4(request):
    return render(request, template_name='hello.html')

def index(request):
    return render(request, 'index.html', )


def movies(request):
    g = request.GET.get('genre', '')
    c = request.GET.get('country', '')
    genres = Genre.objects.all()
    if g != '' and c != '':
        g = int(g)
        c = int(c)
        if Genre.objects.filter(id=g).exists() and Country.objects.filter(id=c).exists():
            genre = Genre.objects.get(id=g)
            country = Country.objects.get(id=c)
            movie_list = Movie.objects.filter(genres=genre, countries=country)
            context = {'movies': movie_list, 'genres': genres, 'filtered_by': f'podle žánru {genre} a země {country}.'}
            return render(request, 'movies.html', context)
    if g != '':
        g = int(g)
        if Genre.objects.filter(id=g).exists():
            genre = Genre.objects.get(id=g)
            context = {'movies': genre.movies_of_genre.all(), 'genres': genres, 'filtered_by': f'podle žánru {genre}'}
            return render(request, 'movies.html', context)
        else:
            context = {'movies': [], 'genres': genres,  'filtered_by': ''}
            return render(request, 'movies.html', context)

    if c != '':
        c = int(c)
        if Country.objects.filter(id=c).exists():
            country = Country.objects.get(id=c)
            context = {'movies': country.movies_in_country.all(), 'genres': genres, 'filtered_by': f'podle země {country}'}
            return render(request, 'movies.html', context)
        else:
            context = {'movies': [], 'genres': genres, 'filtered_by': ''}
            return render(request, 'movies.html', context)

    movies_list = Movie.objects.all()
    genre_list = Genre.objects.all()
    context = {'movies': movies_list, 'genres': genre_list,  'filtered_by': ''}
    return render(request, 'movies.html', context)

def movies_by_genre(request, pk):
    genre_movies = Genre.objects.get(id=pk)
    genre_list = Genre.objects.all()
    context = {'movies': genre_movies.movies_of_genre.all(), 'genres': genre_list}
    return render(request, 'movies.html', context)

def movies_by_country(request, pk):
    country_movies = Country.objects.get(id=pk)
    country_list = Country.objects.all()
    genre_list = Genre.objects.all()
    context = {'movies': country_movies.movies_in_country.all(), 'countries': country_list, 'genres': genre_list}
    return render(request, 'movies.html', context)

def movie(request, pk):
    movie_object = Movie.objects.get(id=pk)
    context = {'movie': movie_object}
    return render(request, 'movie.html', context)

def actors(request):
    actors_object = Person.objects.filter(acting_in_movie__isnull=False).distinct()
    directors_objects = Person.objects.filter(directing_movie__isnull=False).distinct()
    context = {'actors': actors_object, 'directors': directors_objects}
    return render(request, 'actors.html', context)



def actor(request, pk):
    actor_object = Person.objects.get(id=pk)
    context = {'actor': actor_object}
    return render(request, 'actor.html', context)
