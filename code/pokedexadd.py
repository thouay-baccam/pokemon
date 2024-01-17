import pygame
import os
import sys
import json
import tkinter as tk
from tkinter import filedialog
from .file_paths import (
    font_directory,
    backgrounds_directory,
    data_directory,
    pkmnsprites_directory,
)

# Constantes pour les dimensions et les positions
WINDOW_SIZE = (800, 600)
INPUT_RECT_WIDTH_PERCENTAGE = 0.65


class PokedexAdd:
    def __init__(self):
        pygame.init()
        self.window_size = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Ajouter un Pokémon")

        # Loading the background image
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "addpokedex.jpg")
        )
        self.background = pygame.transform.scale(self.background, self.window_size)

        # Setting up the fonts
        self.text_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 24)
        self.input_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 18)

        # Définition du rectangle de l'input field
        self.input_rect = pygame.Rect(
            (self.window_size[0] - (self.window_size[0] * INPUT_RECT_WIDTH_PERCENTAGE))
            // 2,
            250,
            self.window_size[0] * INPUT_RECT_WIDTH_PERCENTAGE,
            40,
        )
        self.input_text = ""
        self.image_directory = ""

        # Texte au-dessus de l'input field
        self.text = self.text_font.render("Nom du Pokémon:", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.window_size[0] // 2, self.window_size[1] // 4)
        )

        # Bouton pour ajouter une image
        self.add_image_text = self.text_font.render(
            "Ajouter une Image", True, (0, 0, 0)
        )
        add_image_text_rect = self.add_image_text.get_rect()
        add_image_text_x = (self.window_size[0] - add_image_text_rect.width) // 2
        add_image_text_y = 350
        self.add_image_button_rect = pygame.Rect(
            add_image_text_x,
            add_image_text_y,
            add_image_text_rect.width,
            add_image_text_rect.height,
        )

        # Bouton pour sauvegarder le Pokémon
        self.save_button_text = self.text_font.render("Sauvegarder", True, (0, 0, 0))
        save_button_text_rect = self.save_button_text.get_rect()
        save_button_text_x = (self.window_size[0] - save_button_text_rect.width) // 2
        save_button_text_y = 450
        self.save_button_rect = pygame.Rect(
            save_button_text_x,
            save_button_text_y,
            save_button_text_rect.width,
            save_button_text_rect.height,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_image_button_rect.collidepoint(event.pos):
                    self.open_file_dialog()
                elif self.save_button_rect.collidepoint(event.pos):
                    self.save_pokemon()

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_directory = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if file_directory:
            self.image_directory = file_directory

    def save_pokemon(self):
        new_pokemon = {"name": self.input_text, "image_directory": self.image_directory}
        # Add logic to save the new_pokemon data to your pokedex.json or relevant data structure.
        with open(os.path.join(data_directory, "pokedex.json"), "r+") as file:
            pokedex = json.load(file)
            pokedex.append(new_pokemon)  # Assuming it's a list in the JSON
            file.seek(0)  # Resets file position to the beginning.
            json.dump(pokedex, file, indent=4)
            file.truncate()  # Truncate file to new length if necessary.

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()

            # Affiche le fond
            self.screen.blit(self.background, (0, 0))

            # Affiche le texte et le champ d'entrée
            self.screen.blit(self.text, self.text_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)

            # Affiche le texte saisi
            input_text_surface = self.input_font.render(
                self.input_text, True, (0, 0, 0)
            )
            input_text_rect = input_text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(input_text_surface, input_text_rect)

            # Affiche les boutons
            pygame.draw.rect(self.screen, (255, 255, 255), self.add_image_button_rect)
            self.screen.blit(self.add_image_text, self.add_image_button_rect.topleft)

            pygame.draw.rect(self.screen, (255, 255, 255), self.save_button_rect)
            self.screen.blit(self.save_button_text, self.save_button_rect.topleft)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pokedex_add = PokedexAdd()
    pokedex_add.run()
