import requests

def get_poke_json(search_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{search_name}'
    response = requests.get(url)

    if response.status_code == 200:
        poke_json = response.json()
        if 'name' in poke_json:
            if poke_json['name'] == search_name:
                return poke_json

    return {}

def get_species_json(poke_json):
    url = poke_json['species']['url']
    response = requests.get(url)
    return response.json()

def get_evolution_chain_json(species_json):
    url = species_json['evolution_chain']['url']
    response = requests.get(url)
    return response.json()
    
def get_next_evolution(species_name, chain_list):
    evolves_to_list = []

    if chain_list:
        for chain_item in chain_list:
            if chain_item['species']['name'] == species_name:
                evolves_to_list = [ item['species']['name'] for item in chain_item['evolves_to'] ]
                return ", ".join(evolves_to_list)
            
        for chain_item in chain_list:
            return_value = get_next_evolution(species_name, chain_item['evolves_to'])
            if return_value:
                return return_value
    else:
        return ''
    



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

    # Evolves From
    evolves_from = species_json['evolves_from_species']
    if evolves_from:
        poke['evolves_from'] = evolves_from['name']

    # Evolves to
    evolution_chain_json = get_evolution_chain_json(species_json)
    initial_chain_list = [evolution_chain_json['chain']]
    evolves_to = get_next_evolution(species_json['name'], initial_chain_list)
    
    if evolves_to:
        poke['evolves_to'] = evolves_to

    # Description
    entry = species_json['flavor_text_entries'][0]
    description = entry['flavor_text'].replace('\x0c', ' ')
    description_lang = entry['language']['name']

    if description:
        poke['description'] = description
        poke['description_lang'] = description_lang



    return poke


def get_pokemon(search_name):
    poke_json = get_poke_json(search_name)

    if poke_json:
        return get_poke_from_json(poke_json)
    else:
        return ''