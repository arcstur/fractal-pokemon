from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

pokemon_list = [
    {
        'name': 'Bulbasaur',
        'type1': 'grass',
        'type2': 'poison',
        'stats': {
            'hp': 62,
            'attack': 62,
            'defense': 32,
            'special_attack': 33,
            'special_defense': 17,
            'speed': 25
        },
        'img': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
        'img_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png',
    },
    {
        'name': 'Charmander',
        'type1': 'fire',
        'type2': '',
        'stats': {
            'hp': 62,
            'attack': 62,
            'defense': 32,
            'special_attack': 33,
            'special_defense': 17,
            'speed': 25
        },
        'img': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',
        'img_shiny': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/4.png',
    }

]

def home(request):
    context = {
        'pokemon_list': pokemon_list,
    }
    return render(request, 'poke_search/home.html', context)

def pokemon(request):
    context = {
        'pokemon': pokemon_list[0],
    }
    return render(request, 'poke_search/pokemon.html', context)

def about(request):
    return HttpResponse('<h1>Sobre</h1>')