import requests
import json
from datetime import datetime
import time
import os

class Pokemon:
    pokemon_api=" https://pokeapi.co/api/v2/pokemon/"
    pokemon_dict=dict()
    def __init__(self,name,id):
        self.name=name
        self.id=id
        self.pokemon_dict={'name':name,'id':id}
    def query_pokemon_api_with_name(self):
        reponse=requests.get(f'{self.pokemon_api}{self.name}').json()
        pokemon=Pokemon(None,None)
        if len(reponse)>0:
            pokemon=Pokemon(reponse['name'],reponse['id'])
            self.pokemon_dict=pokemon.pokemon_dict
        return pokemon
    def query_pokemon_api_with_id(self):
        response = requests.get(f'{self.pokemon_api}{self.id}').json()
        pokemon=Pokemon(None,None)
        if len(response)>0:
            pokemon = Pokemon(response['name'], response['id'])
            self.pokemon_dict = pokemon.pokemon_dict
        return pokemon
    def query_catched_pokemon_with_name(self):
        if Pokemon.check_catched_data_exist():
            f = open('data.json', )
            pokemons = json.load(f)
            f.close()
            for key, value in pokemons.items():
                if (pokemons[key]['name'] == self.name):
                    return pokemons[key]
                else:
                    return None

    def query_catched_pokemon_with_id(self):
        if Pokemon.check_catched_data_exist():
            f = open('data.json', )
            pokemons = json.load(f)
            f.close()
            for key, value in pokemons.items():
                if (pokemons[key]['id'] == self.id):
                    return pokemons[key]
                else:
                    return None
    def find_pokemon_encounters(self):
            if self.name != None:
                pokemon = self.query_pokemon_api_with_name()
                response = requests.get(f'{self.pokemon_api}{pokemon.name}/encounters').json()
                if(len(response)>0):
                    loc=response[0]['location_area']['name']
                    method=response[0]['version_details'][0]['encounter_details'][0]['method']['name']
                else:
                    loc="Not found"
                    method="Not found"
                return loc,method
            elif self.id != None:
                pokemon=self.query_pokemon_api_with_id()
                response = requests.get(f'{self.pokemon_api}{pokemon.id}/encounters').json()
                if (len(response) > 0):
                    loc = response[0]['location_area']['name']
                    method = response[0]['version_details'][0]['encounter_details'][0]['method']['name']
                else:
                    loc = "Not found"
                    method = "Not found"
                return loc, method
    def retrieve_pokemon_detail(self):
        if Pokemon.is_json_file_modified_one_day_ago():
            return self.retrieve_pokemon_based_on_api()
        else:
            if self.name != None:
                result=self.query_catched_pokemon_with_name()
                if result==None:
                    result= self.retrieve_pokemon_based_on_api()
                return result
            elif self.id !=None:
                result=self.query_catched_pokemon_with_id()
                if result==None:
                    result=self.retrieve_pokemon_based_on_api()
                return result
    def retrieve_pokemon_based_on_api(self):
        loc, method = self.find_pokemon_encounters()
        self.pokemon_dict.update({'counter method': method, 'location': loc})
        return self.pokemon_dict
    @classmethod
    def catche_all_pokemon(cls):
        pokemon_json_api = requests.get(cls.pokemon_api).json()
        pokemon_list=dict()
        for i,result in enumerate(pokemon_json_api['results']):
            encounters=requests.get(f'{result["url"]}/encounters').json()
            if(len(encounters)>0):
                loc=encounters[0]['location_area']['name']
                method=encounters[0]['version_details'][0]['encounter_details'][0]['method']['name']
                pokemon_list.update({i:{'id':i+1,'name':result['name'],'method':method,'location':loc}})
            else:
                pokemon_list.update({i: {'id': i + 1, 'name': result['name'], 'method': "not found", 'location': "not found"}})
        with open('data.json', 'w') as my_data_file:
            json.dump(pokemon_list,my_data_file)
        print("Catched Successfully")
    @staticmethod
    def is_json_file_modified_one_day_ago():
        if Pokemon.check_catched_data_exist():
            path=r"data.json"
            time_modified_float=os.path.getmtime(path)
            modified_time=time.ctime(time_modified_float)
            time_obj = time.strptime(modified_time)
            modified_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)
            modified_timestamp_to_datetime=datetime.strptime(modified_timestamp,"%Y-%m-%d %H:%M:%S")
            diff=datetime.now()-modified_timestamp_to_datetime
            hours_diff = divmod(diff.seconds, 3600)
            return hours_diff[0]>=24
        return Pokemon.check_catched_data_exist()
    @staticmethod
    def check_catched_data_exist():
        return os.path.isfile(r"data.json")


