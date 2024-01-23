import pygame
import os
from .file_paths import backgrounds_directory, font_directory

# Constants for the window size and layout
WINDOW_SIZE = (960, 600)
FONT_SIZE = 16  # Adjust as needed
FONT_COLOR = (0, 0, 0)  # Black color for text

class Battle:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Battle")

        # Load the new background image with the battle cards included
        self.bg_image = pygame.image.load(os.path.join(backgrounds_directory, "battlebg.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, WINDOW_SIZE)

        # Font setup
        self.font = pygame.font.Font(os.path.join(font_directory, "pkmn.ttf"), FONT_SIZE)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.bg_image, (0, 0))

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    battle = Battle()
    battle.run()
