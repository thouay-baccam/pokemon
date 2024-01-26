import os
import pygame
import json
from os.path import exists
from file_paths import pokemon_path, save_path, pkmnsprites_directory
from battle_prototype import Battle

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokemon Game")

# Load Pokemon Data
with open(pokemon_path, "r") as file:
    pokemons = json.load(file)

# Create a list of Pokemon names
pokemon_names = [pokemon['name'] for pokemon in pokemons]

# Load Pokemon Sprites
pokemon_sprites = {}
for pokemon in pokemons:
    sprite_path = os.path.join(pkmnsprites_directory, f"{pokemon['name']}.png")
    if os.path.exists(sprite_path):
        pokemon_sprites[pokemon['name']] = pygame.image.load(sprite_path)


# UI Variables
font = pygame.font.Font(None, 36)
current_selection = 0
running = True
show_popup = False

def draw_pokemon_sprites():
    # Get the sprite for the currently selected Pokemon
    sprite = pokemon_sprites.get(pokemon_names[current_selection])
    if sprite:
        # Calculate x and y positions based on the screen size and sprite dimensions
        sprite_width = sprite.get_width()
        sprite_height = sprite.get_height()
        x_position = (screen.get_width() - sprite_width) // 2
        y_position = (screen.get_height() - sprite_height) // 2 - 100  # Adjusted for better placement

        # Draw the sprite
        screen.blit(sprite, (x_position, y_position))

        # Draw the name of the Pokemon below the sprite
        name_text = font.render(pokemon_names[current_selection], True, (0, 0, 0))
        name_text_width = name_text.get_width()
        name_x_position = (screen.get_width() - name_text_width) // 2
        name_y_position = y_position + sprite_height + 10  # 10 pixels below the sprite
        screen.blit(name_text, (name_x_position, name_y_position))



def draw_popup():
    pygame.draw.rect(screen, (200, 200, 200), [250, 200, 300, 200])
    text = font.render("Overwrite save? [Y/N]", True, (0, 0, 0))
    screen.blit(text, (300, 250))

def create_save(pokemon_index):
    new_save = [pokemons[pokemon_index]]
    new_save[0]["level"] = 5  # Set level to 5 for the chosen Pokemon

    with open(save_path, "w") as file:
        json.dump(new_save, file, indent=4)

def start_battle():
    # Initiate the battle sequence
    Battle()

def is_save_file_non_empty():
    return exists(save_path) and os.path.getsize(save_path) > 0

# Main Game Loop
while running:
    screen.fill((255, 255, 255))  # White background

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_selection = (current_selection - 1) % len(pokemon_names)
            elif event.key == pygame.K_RIGHT:
                current_selection = (current_selection + 1) % len(pokemon_names)
            elif event.key == pygame.K_RETURN:
                if is_save_file_non_empty():
                    show_popup = True
                else:
                    create_save(current_selection)
                    start_battle()

        if show_popup:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # Yes, overwrite save
                    show_popup = False
                    create_save(current_selection)
                    start_battle()
                elif event.key == pygame.K_n:
                    # No, don't overwrite
                    show_popup = False

    # Drawing
    draw_pokemon_sprites()
    if show_popup:
        draw_popup()

    # Update the display
    pygame.display.flip()

pygame.quit()