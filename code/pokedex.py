import pygame
import os
import json
import sys
from .file_paths import (
    font_directory,
    music_directory,
    backgrounds_directory,
    data_directory,
    pkmnsprites_directory,
)


class Pokedex:
    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.running = True
        pygame.display.set_caption("Pokédex")

        # Load the background image for the Pokedex
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "pokedex.png")
        )
        self.background = pygame.transform.scale(self.background, self.window_size)

        # Define areas for the list and the information
        self.list_area_rect = pygame.Rect(50, 100, 300, 400)
        self.info_area_rect = pygame.Rect(450, 100, 300, 400)

        self.load_resources()
        self.selected_pokemon = None
        self.selected_pokemon_index = 0  # Index for the selected Pokémon
        self.sprites = self.load_pokemon_sprites()

        pygame.mixer.music.load(os.path.join(music_directory, "pokedex.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Scroll variables
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = len(self.pokedex) * 30 - self.list_area_rect.height

        self.types = {
        '0': "No Type",
        '1': "Normal",
        '2': "Fire",
        '3': "Water",
        '4': "Electric",
        '5': "Grass",
        '6': "Ice",
        '7': "Fight",
        '8': "Poison",
        '9': "Ground",
        '10': "Flying",
        '11': "Psychic",
        '12': "Bug",
        '13': "Rock",
        '14': "Ghost",
        '15': "Dragon",
        '16': "Dark",
        '17': "Steel",
    }

    def load_resources(self):
        """Load resources such as pokedex data and fonts."""
        with open(os.path.join(data_directory, "pokedex.json"), "r") as pokedex_file:
            self.pokedex = json.load(pokedex_file)
        self.text_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 20)

    def load_pokemon_sprites(self):
        """Load pokemon sprites into a dictionary."""
        sprites = {}
        for pokemon in self.pokedex:
            pokemon_name = pokemon["name"].lower()
            sprite_path = os.path.join(pkmnsprites_directory, f"{pokemon_name}.png")
            if os.path.exists(sprite_path):
                sprites[pokemon_name] = pygame.image.load(sprite_path)
        return sprites

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_y = max(self.scroll_y - self.scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    self.scroll_y = min(
                        self.scroll_y + self.scroll_speed, self.max_scroll
                    )
                self.selected_pokemon_index = self.check_pokemon_selection(event.pos)
                self.selected_pokemon = self.pokedex[self.selected_pokemon_index]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_pokemon_index = min(
                        self.selected_pokemon_index + 1, len(self.pokedex) - 1
                    )
                    self.scroll_y = min(
                        self.scroll_y + self.scroll_speed, self.max_scroll
                    )
                elif event.key == pygame.K_UP:
                    self.selected_pokemon_index = max(
                        self.selected_pokemon_index - 1, 0
                    )
                    self.scroll_y = max(self.scroll_y - self.scroll_speed, 0)
                elif event.key == pygame.K_RETURN:
                    self.selected_pokemon = self.pokedex[self.selected_pokemon_index]
                    print(self.selected_pokemon_index)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def check_pokemon_selection(self, mouse_pos):
        """Check if a pokemon in the list has been selected."""
        list_start_y = self.list_area_rect.top - self.scroll_y
        for i, pokemon in enumerate(self.pokedex):
            pokemon_rect = pygame.Rect(
                self.list_area_rect.left,
                list_start_y + i * 30,
                self.list_area_rect.width,
                30,
            )
            if pokemon_rect.collidepoint(mouse_pos):
                self.selected_pokemon = pokemon
                return i

    def display_pokemon_list(self):
        """Display the scrollable list of pokemon."""
        list_start_y = self.list_area_rect.top - self.scroll_y

        for i, pokemon in enumerate(self.pokedex):
            text = self.text_font.render(pokemon["name"], True, (0, 0, 0))
            text_rect = text.get_rect(
                topleft=(self.list_area_rect.left + 10, list_start_y + i * 30)
            )

            # Highlight the selected Pokémon
            if i == self.selected_pokemon_index:
                pygame.draw.rect(
                    self.screen, (255, 0, 0), text_rect
                )  # Red highlight for selection

            if self.list_area_rect.collidepoint(
                text_rect.topleft
            ) or self.list_area_rect.collidepoint(text_rect.bottomleft):
                self.screen.blit(text, text_rect)

    def display_selected_pokemon_info(self):
        """Display information about the selected pokemon."""
        if self.selected_pokemon:
            # Display the pokemon sprite
            pokemon_name = self.selected_pokemon["name"].lower()
            if pokemon_name in self.sprites:
                sprite = self.sprites[pokemon_name]
                sprite = pygame.transform.scale(sprite, (100, 100))  # Resize sprite
                sprite_rect = sprite.get_rect(
                    center=(self.info_area_rect.centerx, self.info_area_rect.top + 120)
                )
                self.screen.blit(sprite, sprite_rect)

            # Set a consistent horizontal margin for the left alignment of text
            horizontal_margin = 20

            # Adjust the starting y position higher up if needed
            info_y_adjustment = 20
            
            # Calculate the vertical spacing based on the font size and desired line spacing
            line_height = self.text_font.size('A')[1] + 5  # Height of the font + 5 pixels of spacing
            
            # Starting position for the information display
            info_x = self.info_area_rect.left + horizontal_margin
            info_y = self.info_area_rect.top + 240 - info_y_adjustment
            
            # Define the information to be displayed
            info_texts = [
                f"Name: {self.selected_pokemon['name']}",
                f"Region: {self.selected_pokemon['region']}",
                f"Encountered: {'Yes' if self.selected_pokemon['encountered'] else 'No'}",
                f"Type: {self.types[self.selected_pokemon['type_1']]}" +
                    (f" / {self.types[self.selected_pokemon['type_2']]}" if self.selected_pokemon.get("type_2") else ""),
                f"Attack: {self.selected_pokemon['attack_stat']}",
                f"Defense: {self.selected_pokemon['defense_stat']}"
            ]
            
            # Render and blit each line of text
            for i, text in enumerate(info_texts):
                text_surface = self.text_font.render(text, True, (0, 0, 0))
                self.screen.blit(text_surface, (info_x, info_y + i * line_height))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.screen.blit(self.background, (0, 0))
            self.display_pokemon_list()
            self.display_selected_pokemon_info()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pokedex = Pokedex((800, 600))
    pokedex.run()
