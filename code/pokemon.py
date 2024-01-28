import json

from code.file_paths import pokemon_path, save_path, select_sprites, pkmnsprites_directory


class Pokemon:
    def __init__(self, stat_dict):
        self.stat_dict = stat_dict
        self.name = stat_dict["name"]
        self.types = stat_dict["types"]
        self.health = 50
        self.max_health = stat_dict.get("max_health", self.health) 
        self.attack = stat_dict["attack_stat"]
        self.defense = stat_dict["defense_stat"]
        self.level = stat_dict.get("level", 5)
        self.front_sprite = select_sprites(f"{self.name.lower()}.png")
        self.back_sprite = select_sprites(f"{self.name.lower()}-back.png")

        if ("evolution" and "evolution_level") in stat_dict:
            self.evolution = stat_dict["evolution"]
            self.evolution_level = stat_dict["evolution_level"]

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'types': self.types,
            # Add any other relevant attributes
        }

    def set_sprite_paths(self):
        # Construct file paths for front and back sprites
        front_sprite_path = f"{pkmnsprites_directory}/{self.name.lower()}.png"
        back_sprite_path = f"{pkmnsprites_directory}/{self.name.lower()}-back.png"

        return front_sprite_path, back_sprite_path

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
                    pokemon["level"] = self.level
        with open(save_path, "w") as file:
            json.dump(pokemons, file, indent=4)