import pygame
import os
import sys
import json
from code.file.file_paths import font_path, music_path, mainmenuimg_path, data_path

class NouvellePartie:
    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Nouvelle Partie")

        # Chargement du fond d'écran
        self.background = pygame.image.load(os.path.join(mainmenuimg_path, "newgamebackground.jpg"))
        self.background = pygame.transform.scale(self.background, window_size)

        # Animation du fond
        self.background_position = 0
        self.background_speed = 2

        # Définition des polices
        self.text_font = pygame.font.Font(os.path.join(font_path, "pkmn.ttf"), 24)
        self.input_font = pygame.font.Font(os.path.join(font_path, "pkmn.ttf"), 18)
        self.button_font = pygame.font.Font(os.path.join(font_path, "pkmn.ttf"), 40)

        # Définition du rectangle de l'input field
        self.input_rect_width_percentage = 0.65
        self.input_rect = pygame.Rect(
            (self.window_size[0] - (self.window_size[0] * self.input_rect_width_percentage)) // 2,
            250,
            self.window_size[0] * self.input_rect_width_percentage,
            40
        )

        # Texte au-dessus de l'input field
        self.text = self.text_font.render("Quel est ton nom?", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 4))

        # Initialisation de l'input field
        self.input_text = ""
        self.input_active = True  # Pour activer l'input field

        # Bouton "Commencer ma partie" centré en bas
        self.start_button_text = self.button_font.render("COMMENCER MA PARTIE", True, (0, 0, 0))
        button_width, button_height = self.start_button_text.get_size()
        button_x = (self.window_size[0] - button_width) // 2
        button_y = self.window_size[1] - 60 - button_height  # Ajustement pour placer le bouton juste au-dessus du bas
        self.start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.start_button_text_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Initialisation du nom du joueur
        self.player_name = ""

        # Ajout de musique
        pygame.mixer.music.load(os.path.join(music_path, "newgamemusic.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

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
                else:
                    self.input_text += event.unicode  # Ajoute le caractère à l'input_text

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = not self.input_active
                else:
                    self.input_active = False

                if self.start_button_rect.collidepoint(event.pos):
                    self.finish_and_close()

    def finish_and_close(self):
        # Ici, tu peux faire quelque chose avant de fermer l'application
        self.save_player_data()
        pygame.quit()
        sys.exit()

    def save_player_data(self):
        player_data = {"nom": self.input_text}  # Remplacez cela par les données que vous souhaitez sauvegarder
        player_file_path = os.path.join(data_path, "player.json")

        with open(player_file_path, "w") as player_file:
            json.dump(player_data, player_file)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()

            # Animation du fond
            self.background_position -= self.background_speed
            if self.background_position <= -self.window_size[0]:
                self.background_position = 0

            # Affiche le fond
            self.screen.blit(self.background, (self.background_position, 0))
            self.screen.blit(self.background, (self.background_position + self.window_size[0], 0))

            # Affiche le texte et le champ d'entrée
            self.screen.blit(self.text, self.text_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)

            # Affiche le texte saisi
            input_text_surface = self.input_font.render(self.input_text, True, (0, 0, 0))
            input_text_rect = input_text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(input_text_surface, input_text_rect)

            # Affiche le bouton "Commencer ma partie"
            pygame.draw.rect(self.screen, (255, 255, 255), self.start_button_rect)
            self.screen.blit(self.start_button_text, self.start_button_text_rect)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    nouvelle_partie = NouvellePartie((800, 600))
    nouvelle_partie.run()