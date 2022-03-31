from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

pokemons = [
    {
        'name': 'bulbasaur',
        'type1': 'grass',
        'type2': 'poison'
    }

]

def home(request):
    return HttpResponse('<h1>Oiê!</h1>')

def about(request):
    return HttpResponse('<h1>Sobre</h1>')