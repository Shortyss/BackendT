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
from django.contrib import admin
from django.urls import path

from viewer.models import *
from viewer.views import *

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Country)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Person)
admin.site.register(Rating)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello', hello),
    path('hello2/<s>', hello2),
    path('hello3/', hello3),
    path('hello4/', hello4),

    path('movies/', movies, name='movies'),
    path('', index, name='index'),
    path('movie/<pk>/', movie, name='movie'),
]
