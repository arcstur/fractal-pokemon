from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

pokemon_list = [
    {
        'name': 'bulbasaur',
        'type1': 'grass',
        'type2': 'poison'
    },
    {
        'name': 'charmander',
        'type1': 'fire',
        'type2': ''
    }

]

def home(request):
    context = {
        'pokemon_list': pokemon_list,
    }
    return render(request, 'poke_search/home.html', context)

def about(request):
    return HttpResponse('<h1>Sobre</h1>')