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
    movies_list = Movie.objects.all()
    context = {'movies': movies_list}
    return render(request, 'movies.html', context)
