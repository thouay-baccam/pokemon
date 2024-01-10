import pygame
import os
import json
import sys
from ..file.file_paths import data_path, font_path, pkmnsprites_path  # Adjusted for relative import

class Pokedex:
    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Pokédex")

        self.load_resources()
        self.selected_pokemon = None
        self.sprites = self.load_pokemon_sprites()

        # Scroll variables
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = len(self.pokedex) * 30 - 300  # Adjust based on list area height

    def load_resources(self):
        """ Load resources such as pokedex data and fonts. """
        with open(os.path.join(data_path, "pokedex.json"), "r") as pokedex_file:
            self.pokedex = json.load(pokedex_file)
        self.text_font = pygame.font.Font(os.path.join(font_path, "pkmn.ttf"), 20)

    def load_pokemon_sprites(self):
        """ Load pokemon sprites into a dictionary. """
        sprites = {}
        for pokemon in self.pokedex:
            pokemon_name = pokemon["name"].lower()
            sprite_path = os.path.join(pkmnsprites_path, f"{pokemon_name}.png")
            if os.path.exists(sprite_path):
                sprites[pokemon_name] = pygame.image.load(sprite_path)
        return sprites

    def handle_events(self):
        """ Handle user input events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_y = max(self.scroll_y - self.scroll_speed, 0)
                if event.button == 5:  # Scroll down
                    self.scroll_y = min(self.scroll_y + self.scroll_speed, self.max_scroll)

                # Check for Pokémon selection
                self.check_pokemon_selection(event.pos)

    def check_pokemon_selection(self, mouse_pos):
        """ Check if a pokemon in the list has been selected. """
        list_start_y = 50 - self.scroll_y
        for i, pokemon in enumerate(self.pokedex):
            pokemon_rect = pygame.Rect(20, list_start_y + i * 30, 200, 100)
            if pokemon_rect.collidepoint(mouse_pos):
                self.selected_pokemon = pokemon
                break

    def display_pokemon_list(self):
        """ Display the scrollable list of pokemon. """
        list_area = pygame.Rect(20, 50, 200, 300)  # Adjust as needed
        list_start_y = 50 - self.scroll_y

        for i, pokemon in enumerate(self.pokedex):
            text = self.text_font.render(pokemon["name"], True, (0, 0, 0))
            text_rect = text.get_rect(topleft=(30, list_start_y + i * 30))

            if list_area.collidepoint(text_rect.topleft) or list_area.collidepoint(text_rect.bottomleft):
                self.screen.blit(text, text_rect)

    def display_selected_pokemon_info(self):
        """ Display information about the selected pokemon. """
        if self.selected_pokemon:
            pokemon_name = self.selected_pokemon["name"].lower()
            if pokemon_name in self.sprites:
                sprite = self.sprites[pokemon_name]
                sprite = pygame.transform.scale(sprite, (100, 100))  # Resize sprite
                sprite_rect = sprite.get_rect(center=(self.window_size[0] // 2, 100))
                self.screen.blit(sprite, sprite_rect)

            info_y_start = 220
            info_gap = 30
            name = f"Nom: {self.selected_pokemon['name']}"
            region = f"Région: {self.selected_pokemon['region']}"
            encountered = f"Rencontré: {'Oui' if self.selected_pokemon['encountered'] else 'Non'}"

            for i, info in enumerate([name, region, encountered]):
                text = self.text_font.render(info, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.window_size[0] // 2, info_y_start + i * info_gap))
                self.screen.blit(text, text_rect)

    def run(self):
        """ Main loop for the Pokedex application. """
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.display_pokemon_list()
            self.display_selected_pokemon_info()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    pokedex = Pokedex((800, 600))
    pokedex.run()
