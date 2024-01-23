class Pokemon:
    def __init__(
        self,
        name,
        type_1,
        type_2,
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

        # 0=nil 1=nor 2=fir 3=wat 4=ele 5=gra
        # 6=ice 7=fig 8=poi 9=gro 10=fly 11=psy
        # 12=bug 13=roc 14=gho 15=dra 16=dark ste=17
        self.type_1 = type_1
        self.type_2 = type_2

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