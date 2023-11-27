from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def hello(request):
    return HttpResponse("Hello World!")


def hello2(request, s):
    return HttpResponse(f"Hello, {s} world!")


def hello3(request):
    s = request.Get.get('s', '')
    return HttpResponse(f"Hello, {s} world!")
