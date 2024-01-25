import json

from file_paths import pokemon_path, save_path


class Pokemon:
    def __init__(
        self,
        name,
        types,
        attack,
        defense, 
        level, 
        front_sprite,
        back_sprite,
        evolution = None,
        evolution_level = None,
        ):
        self.name = name

        self.types = types
        self.health = 20
        self.attack = attack
        self.defense = defense

        self.level = level

        self.front_sprite = front_sprite
        self.back_sprite = back_sprite

        self.evolution = evolution
        self.evolution_level = evolution_level

    def level_up(self):
        self.level += 1
        pokemons = []
        with open(save_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                if pokemon['name'] == self.name:
                    pokemon['level'] = self.level
        with open(save_path, "w") as file:
            json.dump(pokemons, file, indent=4)
        print(f"{self.name} has leveled up! It is now level {self.level}.")
        self.check_evolution()

    def check_evolution(self):
        print(f"Checking evolution for {self.name}. Current level: {self.level}, Required level: {self.evolution_level}")
        if self.evolution and self.level >= self.evolution_level:
            self.evolve()

    def evolve(self):
        print(f"{self.name} is evolving into {self.evolution}!")
        # Load evolution data
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            evolution_data = {}
            for pokemon in pokemons:
                if pokemon['name'] == self.evolution:
                    evolution_data = pokemon
            if evolution_data:
                self.update_pokemon(evolution_data)
            else:
                print("Evolution data not found.")

    def update_pokemon(self, data):
        print(f"Updating {self.name} to {data['name']}")
        pokemons = []
        with open(save_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                if pokemon['name'] == self.name:
                    pokemon['name'] = data['name']
                    pokemon['types'] = data['types']
                    pokemon['attack_stat'] = data['attack_stat']
                    pokemon['defense_stat'] = data['defense_stat']
                    pokemon['level'] = self.level
                    if (
                        'evolution' in data
                        and 'evolution_level' in data
                    ):
                        pokemon['evolution'] = data['evolution']
                        pokemon['evolution_level'] = data['evolution_level']
                    else:
                        pokemon.pop('evolution')
                        pokemon.pop('evolution_level')
                    break
        with open(save_path, "w") as file:
            json.dump(pokemons, file, indent=4)