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
    return render(request, 'poke_search/home.html')

def about(request):
    return HttpResponse('<h1>Sobre</h1>')