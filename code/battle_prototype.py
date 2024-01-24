import json
from random import choice

from file_paths import pokemon_path
from pokemon import Pokemon


class Battle:
    def __init__(self):
        self.player_pokemon = self.choose_pokemon()
        self.enemy_pokemon = self.random_pokemon()

    def choose_pokemon(self):
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for index, pokemon in enumerate(pokemons):
                print(index, pokemon['name'])
            while True:
                choice = input("Choose a pokemon: ")
                if not choice.isdigit():
                    print("Il faut que le choix soit un nombre valide")
                    continue
                if not int(choice) <= len(pokemons)-1:
                    print("Nombre invalide")
                    continue
                print(f"Vous avez choisi {pokemons[int(choice)]['name']}")
                return pokemons[int(choice)]

    def random_pokemon(self):
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            enemy_pokemon = choice(pokemons)
            return enemy_pokemon


if __name__ == "__main__":
    test = Battle()
    print(f"{test.player_pokemon}\n{test.enemy_pokemon}")