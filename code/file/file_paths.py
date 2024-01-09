import os


# REPERTOIRE PRINCIPAL
pokemon_directory = os.path.abspath(
    os.path.join(__file__, os.pardir, os.pardir, os.pardir)
)


# REPERTOIRE CONTENANT LE CODE
code_directory = os.path.join(pokemon_directory, "code")

# REPERTOIRE CONTENANT CODE CONCERNANT LES FICHIERS
file_directory = os.path.join(code_directory, "file")
save_game_path = os.path.join(file_directory, "save_game.py")
file_paths_path = os.path.join(file_directory, "file_paths.py")

# REPERTOIRE CONTENANT CODE CONCERNANT LE GAMEPLAY
gameplay_directory = os.path.join(code_directory, "gameplay")
combat_path = os.path.join(gameplay_directory, "combat.py")
map_path = os.path.join(gameplay_directory, "map.py")
mouvement_path = os.path.join(gameplay_directory, "mouvement.py")
rencontre_sauvage_path = os.path.join(gameplay_directory, "rencontre_sauvage.py")

# REPERTOIRE CONTENANT CODE CONCERNANT LES MENUS
menu_directory = os.path.join(code_directory, "menu")
menu_pause_path = os.path.join(menu_directory, "menu_pause.py")
menu_principal_path = os.path.join(menu_directory, "menu_principal.py")
nouvelle_partie_path = os.path.join(menu_directory, "nouvelle_partie.py")
pokedex_path = os.path.join(menu_directory, "pokedex.py")

# REPERTOIRE CONTENANT CODE CONCERNANT LES PERSONNAGES
personnage_directory = os.path.join(code_directory, "personnage")
personnage_path = os.path.join(personnage_directory, "personnage.py")
joueur_path = os.path.join(personnage_directory, "joueur.py")
pnj_path = os.path.join(personnage_directory, "pnj.py")
trainer_path = os.path.join(personnage_directory, "trainer.py")
pokecenter_path = os.path.join(personnage_directory, "pokecenter.py")
pokemart_path = os.path.join(personnage_directory, "pokemart.py")
starter_pokeball_path = os.path.join(personnage_directory, "starter_pokeball.py")
pokemon_path = os.path.join(personnage_directory, "pokemon.py")

# REPERTOIRE CONTENANT IMAGES
img_path = os.path.join(pokemon_directory, "img")
pkmnsprites_path = os.path.join(img_path, "pkmnsprites")
mainmenuimg_path = os.path.join(img_path, "mainmenuimg")

# REPERTOIRE CONTENANT MUSIQUE
music_path = os.path.join(pokemon_directory, "music")

def select_sprites(image):
    if not isinstance(image, str):
        raise ValueError("Le nom du fichier doit être un string")
    return os.path.join(pkmnsprites_path, image)
