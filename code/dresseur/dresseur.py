from code.dresseur.pokemon import Pokemon


class Dresseur:
    def __init__(self, name, pokemon_list):
        # Si on a le temps, ajouter sprites pour trainer?
        if not isinstance(name, str):
            raise ValueError("Le nom du dresseur doit être un string")
        if not isinstance(pokemon_list, list):
            raise ValueError("Les pokemons du dresseurs doivent être dans une liste")
        for pokemon in pokemon_list:
            if not isinstance(pokemon, Pokemon):
                raise ValueError(
                    "Les pokemons doivent être des instances de la classe Pokemon"
                )
        if len(pokemon_list) > 8:
            raise ValueError("Un dresseur ne peut pas avoir plus de 8 pokemons")

        self.name = name
        self.pokemon_list = pokemon_list
        # Pour les potions hp, faudra peut-être tweak pour balance
        self.potions_number = 10
