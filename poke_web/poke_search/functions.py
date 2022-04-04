import requests
from difflib import get_close_matches
from django.core.cache import cache

def get_name_list():
    cache_key = 'pokemon_name_list'
    pokemon_name_list = cache.get(cache_key)

    if not pokemon_name_list:
        pokemon_name_list = []

        response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=-1')

        for name_dict in response.json()['results']:
            name, url = name_dict.values()
            pokemon_name_list.append(name)
        
        cache.set(cache_key, pokemon_name_list)

    return pokemon_name_list

def get_pokemon_list(search_name):
    correct_name_list = get_name_list()
    input_name_list = get_close_matches(search_name, correct_name_list, n=3)

    pokemon_list = []

    if input_name_list:
        for name in input_name_list:
            pokemon = get_poke_from_correct_name(name)
            if pokemon: pokemon_list.append(pokemon)

    return pokemon_list
            
def get_poke_from_correct_name(correct_name):
    cache_key = f'pokemon_{correct_name}'
    poke_json = cache.get(cache_key)

    if poke_json:
        return get_poke_from_json(poke_json)
    else:
        url = f'https://pokeapi.co/api/v2/pokemon/{correct_name}'
        response = requests.get(url)

        if response.status_code == 200:
            poke_json = response.json()
            cache.set(cache_key, poke_json)
            return get_poke_from_json(poke_json)
        else:
            return ''

def get_species_json(poke_json):
    url = poke_json['species']['url']
    response = requests.get(url)
    return response.json()

def get_evolution_chain_json(species_json):
    url = species_json['evolution_chain']['url']
    response = requests.get(url)
    return response.json()
    
def get_next_evolution(species_name, chain_list):
    if chain_list:
        for chain_item in chain_list:
            if chain_item['species']['name'] == species_name:
                evolves_to_list = [ item['species']['name'].capitalize() for item in chain_item['evolves_to'] ]
                return ", ".join(evolves_to_list)
            
        for chain_item in chain_list:
            return_value = get_next_evolution(species_name, chain_item['evolves_to'])
            if return_value:
                return return_value
    else:
        return ''
    
def get_description(species_json):
    entries = species_json['flavor_text_entries']
    for i, entry in enumerate(entries):
        lang = entry['language']['name']

        if lang in ('en', 'pt') or (i+1 == len(entries)):
            return entry['flavor_text'].replace('\x0c', ' ').replace('\n', ' '), lang

def get_poke_from_json(poke_json):
    poke = {}

    # Name
    poke['name'] = poke_json['name'].capitalize()

    # Types
    poke['type1'] = poke_json['types'][0]['type']['name']
    poke['type2'] = ''

    if len(poke_json['types']) > 1:
        poke['type2'] = poke_json['types'][1]['type']['name']

    # Stats
    poke['stats'] = {}
    for stat in poke_json['stats']:
        stat_name = stat['stat']['name'].replace('-', '_')
        poke['stats'][stat_name] = stat['base_stat']

    # Default Img
    poke['img'] = poke_json['sprites']['front_default']

    # Shiny Img
    poke['img_shiny'] = poke_json['sprites']['front_shiny']

    # Species Json
    species_json = get_species_json(poke_json)

    # Gender
    gender_rate = int(species_json['gender_rate'])

    poke['genders'] = {}
    poke['genders']['masc'] = (0 <= gender_rate < 8)
    poke['genders']['fem'] = (0 < gender_rate <= 8)
    poke['genders']['genderless'] = (gender_rate == -1)

    # Gender Img
    if species_json['has_gender_differences']:
        poke['img_female'] = poke_json['sprites']['front_female']
        poke['img_shiny_female'] = poke_json['sprites']['front_shiny_female']

    # Evolves From
    evolves_from = species_json['evolves_from_species']
    if evolves_from:
        poke['evolves_from'] = evolves_from['name'].capitalize()

    # Evolves to
    evolution_chain_json = get_evolution_chain_json(species_json)
    initial_chain_list = [evolution_chain_json['chain']]
    evolves_to = get_next_evolution(species_json['name'], initial_chain_list)
    
    if evolves_to:
        poke['evolves_to'] = evolves_to

    # Description
    description, description_lang = get_description(species_json)

    if description:
        poke['description'] = description
        poke['description_lang'] = description_lang



    return poke