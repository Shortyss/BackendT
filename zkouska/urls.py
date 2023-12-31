"""
URL configuration for zkouska project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.templatetags import rest_framework

import api
from api.views import *
from accounts.views import *
from viewer.models import *
from viewer.views import *
from zkouska import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello', hello),
    path('hello2/<s>', hello2),
    path('hello3/', hello3),
    path('hello4/', hello4),

    path('', index, name='index'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),     # defaultní views pro přihlašování/odhlašován/...

    path('accounts/profile_create/<pk>', ProfileCreateView.as_view(), name='profile_create'),
    path('accounts/profile/<pk>/', profile, name='profile'),
    path('accounts/profile_edit/', profile_edit, name='profile_edit'),


    path('News/', news, name='News'),
    path('NewsOnDVD', newsOnDVD, name='NewsOnDVD'),
    path('movies/', MoviesListView.as_view(), name='movies2'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('administration/', administration, name='administration'),
    path('country_admin/', CountryView.as_view(), name='country_admin'),
    path('movies_admin/', MoviesView.as_view(), name='movies_admin'),
    # path('movies/', MoviesTemplateView.as_view(), name=MoviesTemplateView),
    # path('movies2/', MoviesListView.as_view(), name=MoviesListView),
    path('movie/<pk>/', movie, name='movie'),
    path('movie/update/<pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>/', MovieDeleteView.as_view(), name='movie_delete'),
    path('actors/', actors, name='actors'),
    path('actor/<pk>/', actor, name='actor'),
    #path('person/create/', PersonCreateView.as_view(), name='person_create'),
    path('genre_admin/', GenresView.as_view(), name='genre_admin'),
    path('genre/<pk>/', movies_by_genre, name='genre'),
    path('genre/update/<pk>', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genre/delete/<pk>/', GenreDeleteView.as_view(), name='genre_delete'),
    path('country/<pk>/', movies_by_country, name='country'),
    # path('administration/', CountryView.as_view(), name='country_view'),
    path('countries/create/', CountryCreateView.as_view(), name='create_country'),
    path('countries/delete/<pk>/', CountryDeleteView.as_view(), name='country_delete'),
    path('countries/update/<pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('persons_admin/', PersonsView.as_view(), name='persons_admin'),
    path('person/create/', PersonCreateView.as_view(), name='person_create'),
    #path('person/create/', PersonModelForm, name='person_create'),
    path('actor/update/<pk>/', PersonUpdateView.as_view(), name='person_update'),
    path('person/delete/<pk>/', PersonDeleteView.as_view(), name='person_delete'),
    path('person/<pk>/', person, name='person'),

    path('rate_movie/', rate_movie, name='rate_movie'),
    path('add_comment/', add_comment, name='add_comment'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/movies/', api.views.Movies.as_view()),

    path('api/movie/<pk>/', api.views.MovieDetail.as_view()),

    path('api/person/<pk>/', api.views.PersonDetail.as_view()),
    path('api/persons/', api.views.PersonsList.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
