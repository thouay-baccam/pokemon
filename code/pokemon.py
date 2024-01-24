class Pokemon:
    def __init__(
        self,
        name,
        types,
        health,
        attack,
        defense, 
        level, 
        exp, 
        front_sprite,
        back_sprite,
        evolution = None,
        evolution_level = None,
        ):
        self.name = name

        self.types = types
        self.health = health
        self.attack = attack
        self.defense = defense

        self.level = level

        self.front_sprite = front_sprite
        self.back_sprite = back_sprite

        self.evolution = evolution
        self.evolution_level = evolution_level