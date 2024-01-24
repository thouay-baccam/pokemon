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
        self.exp = exp

        self.front_sprite = front_sprite
        self.back_sprite = back_sprite

        self.evolution = evolution
        self.evolution_level = evolution_level

    def gain_exp(self):
        self.exp += 100
        if not self.exp >= 100 * self.level:
            return
        self.exp = 0
        self.level += 1