from logging import getLogger
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.base import ContentFile
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper

from viewer.models import *
from django.forms import Form, DateField, ModelChoiceField, Textarea, CharField, IntegerField, ModelMultipleChoiceField, \
    ImageField, SelectDateWidget, ModelForm, DateInput, SelectMultiple

from django import forms
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


# Create your views here.

LOGGER = getLogger()



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


def news(request):
    return render(request, 'News.html', )


def newsOnDVD(request):
    return render(request, 'NewsOnDVD.html', )

@login_required
def administration(request):
    return render(request, 'administration.html', )


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


class MoviesView(View):
    def get(self, request):
        movies_list = Movie.objects.all()
        context = {'movies': movies_list}
        return render(request, 'movies_admin.html', context)


class MoviesTemplateView(TemplateView):
    template_name = 'movies.html'
    extra_context = {'movies': Movie.objects.all()}


class MoviesListView(ListView):
    template_name = 'movies2.html'
    model = Movie
    paginate_by = 1


class MovieModelForm(LoginRequiredMixin, ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'

        widgets = {
            'countries': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('create_country')
            ),
            'genres': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('genre_create')
            ),
            'directors': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('person_create')
            ),
            'actors': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('person_create')
            )
        }

        labels = {
            'title_orig': 'Originální název'
        }

        help_text = {
            'title_orig': 'Zadejte originální název'
        }

        error_messages = {
            'title_orig': {
                'max_length': 'Název je příliš dlouhý'
            }
        }

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'movie_create.html'
    model = Movie
    form_class = MovieModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.change_movie'


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.delete_movie'


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
    if Movie.objects.filter(id=pk).count() == 0:
        return reverse_lazy('index')

    try:
        movie_object = Movie.objects.get(id=pk)
    except:
        return render(request, 'movies.html')

    movie_object = Movie.objects.get(id=pk)
    avg_rating = None
    if Rating.objects.filter(movie=movie_object).count() > 0:
        avg_rating = Rating.objects.filter(movie=movie_object).aggregate(Avg('rating'))

    # hodnocení daného uživatele
    user = request.user
    user_rating = None
    if request.user.is_authenticated:
        if Rating.objects.filter(movie=movie_object, user=user).count() > 0:
            user_rating = Rating.objects.get(movie=movie_object, user=user)

    comments = Comment.objects.filter(movie=movie_object).order_by('-created')

    images = Image.objects.filter(movie=movie_object)

    context = {'movie': movie_object, 'avg_rating': avg_rating,
               'user_rating': user_rating, 'comments': comments, 'images': images}
    return render(request, 'movie.html', context)


class GenreModelForm(ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().capitalize()
        return name


class GenresView(View):
    def get(self, request):
        genres_list = Genre.objects.all()
        context = {'genres': genres_list}
        return render(request, 'genre_admin.html', context)


class GenreCreateView(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'genre_create.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.add_genre'


class GenreUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'genre_admin.html'
    model = Genre
    form_class = GenreModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.change_genre'


class GenreDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'
    model = Genre
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.delete_genre'


class CountryModelForm(ModelForm):

    class Meta:
        model = Country
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().capitalize()
        return name


class CountryCreateView(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'country_create.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.add_country'


class CountryView(View):
    def get(self, request):
        countries_list = Country.objects.all()
        context = {'countries': countries_list}
        return render(request, 'country_admin.html', context)


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'country_admin.html'
    model = Country
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.change_country'


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'country_confirm_delete.html'  # TODO country_confirm_delete.html
    model = Country
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.delete_country'


class MovieForm(Form):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64, required=False)
    title_sk = CharField(max_length=64, required=False)
    countries = ModelMultipleChoiceField(queryset=Country.objects)
    genres = ModelMultipleChoiceField(queryset=Genre.objects)
    directors = ModelMultipleChoiceField(queryset=Person.objects)
    actors = ModelMultipleChoiceField(queryset=Person.objects)
    year = DateField(widget=SelectDateWidget(years=range(1900, datetime.now().year + 4)), label='Date of publication')
    video = CharField(max_length=128, required=False)
    description = CharField(widget=Textarea, required=False)

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()   #  odstraní prázdné znaky na začátku a na konci
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieCreateView(LoginRequiredMixin, FormView):
    template_name = 'movie_create.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movis')
    permission_required = 'viewer.add_movie'


    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        new_movie = Movie.objects.create(
            title_orig=cleaned_data['title_orig'],
            title_cz=cleaned_data['title_cz'],
            title_sk=cleaned_data['title_sk'],
            image=cleaned_data['image'],
            # countries=cleaned_data['countries'],
            # genres=cleaned_data['genres'],
            # directors=cleaned_data['directors'],
            # actors=cleaned_data['actors'],
            year=cleaned_data['year'],
            video=cleaned_data['video'],
            description=cleaned_data['description']
        )

        new_movie.countries.set(cleaned_data['countries'])
        new_movie.genres.set(cleaned_data['genres'])
        new_movie.directors.set(cleaned_data['directors'])
        new_movie.actors.set(cleaned_data['actors'])

        if 'image' in self.request.FILES:
            image_file = self.request.FILES['image']
            # Vytvoření názvu souboru na základě slugifikovaného názvu filmu
            image_name = slugify(new_movie.title_orig) + '.' + image_file.name.split('.')[-1]
            new_movie.image.save(image_name, ContentFile(image_file.read()), save=True)

        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


def actors(request):
    actors_object = Person.objects.filter(acting_in_movie__isnull=False).distinct()
    directors_objects = Person.objects.filter(directing_movie__isnull=False).distinct()
    context = {'actors': actors_object, 'directors': directors_objects}
    return render(request, 'actors.html', context)


def actor(request, pk):
    actor_object = Person.objects.get(id=pk)

    images = Image.objects.filter(actor=actor_object)

    context = {'actor': actor_object, 'images': images}
    return render(request, 'actor.html', context)


class PersonForm(Form):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    nationality = CharField(max_length=64)
    birth_date = DateField(widget=SelectDateWidget(years=range(1900, datetime.now().year + 1)), label='Birth Date')
    date_of_death = DateField(widget=SelectDateWidget(years=range(1900, datetime.now().year + 1)), required=False, label='Date of Death')
    biography = CharField(widget=forms.Textarea)

    def clean_first_name(self):
        initial_form = super().clean()
        initial = initial_form['first_name'].strip()   #  odstraní prázdné znaky na začátku a na konci
        return initial.capitalize()

    def clean_last_name(self):
        initial_form = super().clean()
        initial = initial_form['last_name'].strip()   #  odstraní prázdné znaky na začátku a na konci
        return initial.capitalize()

    def clean(self):
        return super().clean()


class PersonModelForm(LoginRequiredMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'dd-mm-yyyy',
                'class': 'form-control'
            }
        )

    class Meta:
        model = Person
        fields = '__all__'  # ve formuláři budou všechny atributy
        # fields = ['last_name', 'first_name']  # ve formuláři se zobrazí pouze tyto atributy (v daném pořadí)
        # exclude = ['biography']  # ve formuláři budou všechny atributy kromě těchto

    def clean_first_name(self):
        initial_data = super().clean()
        initial = initial_data['first_name']
        return initial.capitalize()

    def clean_last_name(self):
        initial_data = super().clean()
        initial = initial_data['last_name']
        return initial.capitalize()


class PersonCreateView(PermissionRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'person_create.html'
    form_class = PersonModelForm
    success_url = reverse_lazy('person_create')
    permission_required = 'viewer.add_person'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)

class PersonsListView(ListView):
    template_name = 'persons_admin.html'
    model = Person


class PersonsView(View):
    def get(self, request):
        persons_list = Person.objects.all()
        context = {'persons': persons_list}
        return render(request, 'persons_admin.html', context)

# TODO: vytvořit CBV, která zvlášť zobrazí herce a zvlášť režiséry


def person(request, pk):
    person_obj = Person.objects.get(id=pk)
    context = {'person': person_obj}
    return render(request, 'person.html', context)




class PersonCreateView1(CreateView):
    template_name = 'person_create.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_create')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'person_create.html'
    model = Person
    form_class = PersonModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.change_person'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'
    model = Person
    success_url = reverse_lazy('administration')
    permission_required = 'viewer.delete_person'


def rate_movie(request):
    user = request.user
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_object = Movie.objects.get(id=movie_id)
        rating = request.POST.get('rating')

        if Rating.objects.filter(movie=movie_object, user=user).count() > 0:
            # aktualizujeme hodnocení
            user_rating = Rating.objects.get(movie=movie_object, user=user)
            user_rating.rating = rating
            user_rating.save()
        else:
            Rating.objects.create(
                movie=movie_object,
                user=user,
                rating=rating
            )
    return redirect(f"/movie/{movie_id}/")


def add_comment(request):
    user = request.user
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        comment = request.POST.get('comment').strip()
        if comment:
            Comment.objects.create(
                movie=movie_obj,
                user=user,
                comment=comment
            )
    return redirect(f"/movie/{movie_id}")

