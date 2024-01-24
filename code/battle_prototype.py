import json
from random import choice

from file_paths import pokemon_path
from pokemon import Pokemon


class Battle:
    def __init__(self):
        self.player_pokemon = self.choose_pokemon()
        self.enemy_pokemon = self.random_pokemon()
        self.type_chart = (
            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5),
            (0,1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2),
            (0,1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1),
            (0,1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1),
            (0,1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5),
            (0,1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5),
            (0,2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2),
            (0,1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0),
            (0,1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2),
            (0,1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5),
            (0,1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5),
            (0,1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5),
            (0,1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5),
            (0,0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5),
            (0,1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5)
        )

    def choose_pokemon(self):
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for index, pokemon in enumerate(pokemons):
                pokemon["types"] = tuple(pokemon["types"])
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
            for pokemon in pokemons:
                pokemon["types"] = tuple(pokemon["types"])
            enemy_pokemon = choice(pokemons)
            return enemy_pokemon


if __name__ == "__main__":
    battle = Battle()
    print(f"{battle.player_pokemon}\n{battle.enemy_pokemon}\n")

    multipliers = []
    for player_type in battle.player_pokemon["types"]:
        for enemy_type in battle.enemy_pokemon["types"]:
            multipliers.append(battle.type_chart[player_type][enemy_type])
    attack_message = (
        f"{battle.player_pokemon["name"]} attacks "
        f"{battle.enemy_pokemon["name"]}\n"
    )
    damage = (battle.player_pokemon["attack_stat"]/battle.enemy_pokemon["defense_stat"])/50+2*max(multipliers)
    
    if max(multipliers) == 2:
        print(f"{attack_message}It is very effective!\n{damage} DMG")
    elif max(multipliers) == 1:
        print(attack_message, f"{damage} DMG")
    elif max(multipliers) == 0.5:
        print(f"{attack_message}It's not very effective...\n{damage} DMG")
    elif max(multipliers) == 0:
        print(f"{attack_message}It doesn't do anything...\n{damage} DMG")