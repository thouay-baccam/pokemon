import json
from random import choice

from file_paths import save_path, pokemon_path
from pokemon import Pokemon


class Combat:
    # player_pokemon est une instance de la classe Pokemon
    def __init__(self, player_pokemon):
        # `fmt` permet de dire à "black" (programme qui gère le format du code)
        # de ne pas toucher au tuple
        # fmt: off

        # Ce tuple est comme un tableau contenant
        # les facteurs par lesquels le dommage est multiplié
        # Basé sur le tableau Gen 2 de pokemondb.net/type
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
        # fmt: on

        self.player_pokemon = player_pokemon
        self.enemy_pokemon = self.random_pokemon()
        self.battle()

    # Méthode pour choisir un pokemon adversaire aléatoirement
    def random_pokemon(self):
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                # Conversion array JSON en tuple Python
                pokemon["types"] = tuple(pokemon["types"])
            enemy_pokemon = choice(pokemons)
            return Pokemon(
                enemy_pokemon["name"],
                enemy_pokemon["types"],
                enemy_pokemon["attack_stat"],
                enemy_pokemon["defense_stat"],
                self.player_pokemon.level,
                # Utiliser select_sprites dans file_path
                "nothing.jpg",
                "go-away.jpg",
            )

    # Eventuellement, on aura plus besoin des prints dans les méthodes
    def print_status(self, pokemon):
        print(
            f"NAME: {pokemon.name}\n"
            f"HP: {pokemon.health}\n"
            f"TYPES: {pokemon.types}\n"
            f"ATK: {pokemon.attack}\n"
            f"DEF: {pokemon.defense}\n"
            f"LVL: {pokemon.level}\n"
        )

    def attack(self, attacker, target):
        multipliers = []
        # Pour obtenir toutes les combinaisons de types
        for attacker_type in attacker.types:
            for target_type in target.types:
                multipliers.append(self.type_chart[attacker_type][target_type])

        # Attaque manqué
        hit_chance = choice(range(0, 4))
        if hit_chance > 0:
            multiplier = max(multipliers)
        else:
            multiplier = 0

        damage = (attacker.attack / target.defense) / 50 + 2 * multiplier
        damage = int(damage)
        target.health -= damage

        attack_message = f"{attacker.name} attacks " f"{target.name}\n"
        messages = {
            2: f"{attack_message}It is very effective!\n{damage} DMG\n",
            1: f"{attack_message}{damage} DMG\n",
            0.5: f"{attack_message}It's not very effective...\n{damage} DMG\n",
            0: f"{attack_message}It missed!\n{damage} DMG\n",
        }
        print(messages[multiplier])

    def battle(self):
        while self.player_pokemon.health > 0 and self.enemy_pokemon.health > 0:
            self.print_status(self.player_pokemon)
            self.print_status(self.enemy_pokemon)
            self.attack(self.player_pokemon, self.enemy_pokemon)

            self.print_status(self.player_pokemon)
            self.print_status(self.enemy_pokemon)
            self.attack(self.enemy_pokemon, self.player_pokemon)

        self.print_status(self.player_pokemon)
        self.print_status(self.enemy_pokemon)

        if self.enemy_pokemon.health <= 0:
            print("The player's Pokemon has won")
            self.player_pokemon.level_up()
        else:
            print("The player's Pokemon has lost")
