from django.shortcuts import render
from django.http import HttpResponse
from .adv import advfunc

# Create your views here.


def response(request):
    advfunc()
    return HttpResponse('hello')
