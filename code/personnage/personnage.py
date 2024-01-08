class Personnage:
    def __init__(self, name, gender, overworld_sprite, battle_sprite, x_pos, y_pos):
        if not isinstance(name, str):
            raise ValueError("Le nom doit être un string")
        if not isinstance(gender, str):
            raise ValueError("Le genre doit être un string")
        if not isinstance(overworld_sprite, str) or not isinstance(battle_sprite, str):
            raise ValueError("Le chemin vers les sprites doivent être des strings")
        if not isinstance(x_pos, int) or not isinstance(y_pos, int):
            raise ValueError("Les coordonnées doivent être des integers.")
        self.name = name
        self.gender = gender  # Le genre devrait "F" ou "M", je pense
        self.overworld_sprite = overworld_sprite
        self.battle_sprite = battle_sprite
        self.x_pos = x_pos
        self.y_pos = y_pos
