import json

from file_paths import pokemon_path, save_path


class Pokemon:
    def __init__(
        self,
        stat_dict
    ):
        self.stat_dict = stat_dict
        self.name = stat_dict['name']

        self.types = stat_dict['types']
        self.health = 20
        self.attack = stat_dict['attack_stat']
        self.defense = stat_dict['defense_stat']

        self.level = stat_dict['level']

        self.front_sprite = "ejaieazjieazijeiazj"
        self.back_sprite = "cxjwklcwxnkxwn"

        if ("evolution" and "evolution_level") in stat_dict:
            self.evolution = stat_dict['evolution']
            self.evolution_level = stat_dict['evolution_level']

    # Méthode pour changer de niveau
    def level_up(self):
        self.level += 1
        pokemons = []
        with open(save_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                if pokemon["name"] == self.name:
                    pokemon["level"] = self.level
        with open(save_path, "w") as file:
            json.dump(pokemons, file, indent=4)
        print(f"{self.name} has leveled up! It is now level {self.level}.")
        self.check_evolution()

    # Méthode pour vérifier evolution
    def check_evolution(self):
        print(
            f"Checking evolution for {self.name}."
            f"Current level: {self.level},"
            f"Required level: {self.evolution_level}"
        )
        if self.evolution and self.level >= self.evolution_level:
            self.evolve()

    # Méthode pour évoluer
    def evolve(self):
        print(f"{self.name} is evolving into {self.evolution}!")
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            evolution_data = {}
            for pokemon in pokemons:
                if pokemon["name"] == self.evolution:
                    evolution_data = pokemon
            if evolution_data:
                self.update_pokemon(evolution_data)
            else:
                print("Evolution data not found.")

    # Méthode pour mettre à jour le pokémon
    def update_pokemon(self, data):
        print(f"Updating {self.name} to {data['name']}")
        pokemons = []
        with open(save_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                if pokemon["name"] == self.name:
                    pokemon = data
                    pokemon['level'] = self.level
        with open(save_path, "w") as file:
            json.dump(pokemons, file, indent=4)
