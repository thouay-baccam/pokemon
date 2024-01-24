import os

# MAIN DIRECTORY
pokemon_directory = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

# DIRECTORY CONTAINING CODE
code_directory = os.path.join(pokemon_directory, "code")
menu_principal_path = os.path.join(os.path.dirname(__file__), "menu_principal.py")

# DIRECTORY CONTAINING DATA FILES
data_directory = os.path.join(pokemon_directory, "data")
pokemon_path = os.path.join(data_directory, "pokemon.json")

# DIRECTORY CONTAINING FONTS
font_directory = os.path.join(pokemon_directory, "font")

# DIRECTORY CONTAINING IMAGES
img_directory = os.path.join(pokemon_directory, "img")
backgrounds_directory = os.path.join(img_directory, "backgrounds")
pkmnsprites_directory = os.path.join(img_directory, "pkmnsprites")

# DIRECTORY CONTAINING MUSIC
music_directory = os.path.join(pokemon_directory, "music")

# UTILITY FUNCTION FOR SELECTING SPRITES
def select_sprites(sprite_name):
    if not isinstance(sprite_name, str):
        raise ValueError("Le nom du fichier doit être un string")
    return os.path.join(pkmnsprites_directory, sprite_name)
