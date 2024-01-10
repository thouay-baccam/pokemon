from code.dresseur.dresseur import Dresseur


class Adversaire(Dresseur):
    def __init__(self, name, pokemon_list):
        super().__init__(name, pokemon_list)

    # AJOUTER METHODES POUR CHOISIR QUOI FAIRE (ATTAQUER, CHANGER PKMN, UTILISER POTIONS)
