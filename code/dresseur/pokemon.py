from code.file.file_paths import pkmnsprites_path


class Pokemon:
    def __init__(self, name, move_dict, health_points, experience, level, sprite_path):
        if not isinstance(name, str):
            raise ValueError("Le nom du pokémon doit être un string")
        if not isinstance(move_dict, dict):
            raise ValueError("Les moves d'un pokemon doivent être dans un dictionnaire")
        if len(move_dict) > 4:
            raise ValueError("Un pokemon ne peut pas avoir plus de 4 moves")
        if not isinstance(health_points, int):
            raise ValueError("L'HP doit être un integer")
        if not isinstance(experience, int):
            raise ValueError("L'XP doit être un integer")
        if not isinstance(level, int):
            raise ValueError("Le niveau doit être un integer")
        if not isinstance(sprite_path, str):
            raise ValueError("Le chemin vers le sprite doit être un string")

        self.name = name
        # Dictionnaire contenant effet du move, AP, chance que ça réussi...
        self.move_dict = move_dict
        self.health_points = health_points
        # Faudra une méthode pour calculer exp nécessaire pour level up
        # Méthode pour check si level up
        self.experience = experience
        self.level = level
        self.sprite = sprite_path
        # Peut être ajouter sons, si on veut flex.
