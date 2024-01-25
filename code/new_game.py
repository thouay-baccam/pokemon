import json
from os.path import exists

from file_paths import pokemon_path, save_path
from battle_prototype import Battle


class NewGame:
    def __init__(self):
        self.check_save()

    def check_save(self):
        if exists(save_path):
            choice = input(
                f"This file already exists, overwrite it?\n"
                f"[Y]es or [N]o? "
            )
            if choice == "Y" or choice == "y":
                self.create_save()
                Battle()
            elif choice == "N" or choice == "n":
                return
            else:
                print("Invalid choice.")
        else:
            self.create_save()
            Battle()

    def create_save(self):
        new_save = []
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)

            new_save.append(pokemons[0])
            new_save.append(pokemons[3])
            new_save.append(pokemons[6])

            for pokemon in new_save:
                pokemon["level"] = 5

        with open(save_path, "w") as file:
            json.dump(new_save, file, indent=4)


if __name__ == "__main__":
    new_game = NewGame()