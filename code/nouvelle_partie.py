import pygame
import os
import sys
import json

# Assuming file_paths.py now provides directory paths
# In nouvelle_partie.py
from .file_paths import (
    font_directory,
    music_directory,
    img_directory,
    backgrounds_directory,
    data_directory,
)


# Constantes pour les dimensions et les positions
WINDOW_SIZE = (800, 600)
INPUT_RECT_WIDTH_PERCENTAGE = 0.65


class NouvellePartie:
    def __init__(self):
        pygame.init()
        self.window_size = WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.window_size)
        self.running = True
        pygame.display.set_caption("Nouvelle Partie")

        # Chargement du fond d'écran
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "newgame.jpg")
        )
        self.background = pygame.transform.scale(self.background, self.window_size)

        # Animation du fond
        self.background_position = 0
        self.background_speed = 2

        # Définition des polices
        self.text_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 24)
        self.input_font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), 18)
        self.button_font = pygame.font.Font(
            os.path.join(font_directory, "pkmn.ttf"), 40
        )

        pygame.mixer.music.load(os.path.join(music_directory, "newgamemusic.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Définition du rectangle de l'input field
        self.input_rect = pygame.Rect(
            (self.window_size[0] - (self.window_size[0] * INPUT_RECT_WIDTH_PERCENTAGE))
            // 2,
            250,
            self.window_size[0] * INPUT_RECT_WIDTH_PERCENTAGE,
            40,
        )

        # Texte au-dessus de l'input field
        self.text = self.text_font.render("Quel est ton nom?", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.window_size[0] // 2, self.window_size[1] // 4)
        )

        # Initialisation de l'input field
        self.input_text = ""
        self.input_active = True

        # Bouton "Commencer ma partie" centré en bas
        self.start_button_text = self.button_font.render(
            "COMMENCER MA PARTIE", True, (0, 0, 0)
        )
        button_width, button_height = self.start_button_text.get_size()
        button_x = (self.window_size[0] - button_width) // 2
        button_y = self.window_size[1] - 60 - button_height
        self.start_button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height
        )
        self.start_button_text_rect = pygame.Rect(
            button_x, button_y, button_width, button_height
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_player_name()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.finish_and_close()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif pygame.K_a <= event.key <= pygame.K_z:
                    self.input_text += event.unicode.upper()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = not self.input_active
                else:
                    self.input_active = False

                if self.start_button_rect.collidepoint(event.pos):
                    self.finish_and_close()

    def finish_and_close(self):
        self.save_player_data()
        self.launch_battle()

    def launch_battle(self):
        from .battle import Battle
        battle = Battle()
        battle.run()

    def save_player_data(self):
        player_data = {"nom": self.input_text}
        player_file_path = os.path.join(data_directory, "player.json")

        with open(player_file_path, "w") as player_file:
            json.dump(player_data, player_file)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()

            # Animation du fond
            self.background_position -= self.background_speed
            if self.background_position <= -self.window_size[0]:
                self.background_position = 0

            # Affiche le fond
            self.screen.blit(self.background, (self.background_position, 0))
            self.screen.blit(
                self.background, (self.background_position + self.window_size[0], 0)
            )

            # Affiche le texte et le champ d'entrée
            self.screen.blit(self.text, self.text_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)

            # Affiche le texte saisi
            input_text_surface = self.input_font.render(
                self.input_text, True, (0, 0, 0)
            )
            input_text_rect = input_text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(input_text_surface, input_text_rect)

            # Affiche le bouton "Commencer ma partie"
            pygame.draw.rect(self.screen, (255, 255, 255), self.start_button_rect)
            self.screen.blit(self.start_button_text, self.start_button_text_rect)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    nouvelle_partie = NouvellePartie()
    nouvelle_partie.run()
