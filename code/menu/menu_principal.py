import pygame
import os
from code.file.file_paths import mainmenuimg_path, music_path, font_path
from code.menu.nouvelle_partie import NouvellePartie

class MainMenu:
    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Main Menu")

        self.logo = pygame.image.load(os.path.join(mainmenuimg_path, "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500, 200))
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (self.window_size[0] // 2, 120)

        self.background = pygame.image.load(os.path.join(mainmenuimg_path, "background.jpg"))
        self.background = pygame.transform.scale(self.background, self.window_size)

        self.background_position = 0
        self.logo_bounce = 0
        self.bounce_direction = 1
        self.selected_button = 0  

        pygame.mixer.music.load(os.path.join(music_path, "mainmenumusic.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.buttons = [
            {"text": "NOUVELLE PARTIE", "position": (self.window_size[0] // 2, 300)},
            {"text": "CONTINUER", "position": (self.window_size[0] // 2, 330)},
            {"text": "AJOUTER UN POKEMON", "position": (self.window_size[0] // 2, 370)},
            {"text": "QUITTER", "position": (self.window_size[0] // 2, 410)}
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.buttons):
                    if (
                        button["position"][0] - 100 < event.pos[0] < button["position"][0] + 100
                        and button["position"][1] - 15 < event.pos[1] < button["position"][1] + 15
                    ):
                        self.button_clicked(button["text"])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    self.button_clicked(self.buttons[self.selected_button]["text"])

    def button_clicked(self, button_text):
        if button_text == "QUITTER":
            pygame.quit()
            sys.exit()
        elif button_text == "NOUVELLE PARTIE":
            self.run_nouvelle_partie()
        else:
            print(f"CE BOUTON NE MARCHE PAS ENCORE: {button_text}")

    def run_nouvelle_partie(self):
        nouvelle_partie = NouvellePartie(self.window_size)
        nouvelle_partie.run()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()

            self.background_position -= 1
            if self.background_position <= -self.window_size[0]:
                self.background_position = 0

            bounce_speed = 0.2

            max_bounce = 10
            if self.logo_bounce > max_bounce:
                self.bounce_direction = -1
            elif self.logo_bounce < -max_bounce:
                self.bounce_direction = 1

            self.logo_bounce += bounce_speed * self.bounce_direction

            self.logo_rect.centery = 120 + self.logo_bounce

            self.screen.blit(self.background, (self.background_position, 0))
            self.screen.blit(self.background, (self.background_position + self.window_size[0], 0))

            self.screen.blit(self.logo, self.logo_rect)

            custom_font = pygame.font.Font(os.path.join(font_path, "pkmn.ttf"), 16)
            for i, button in enumerate(self.buttons):
                text = custom_font.render(button["text"], True, (0, 0, 0))
                text_rect = text.get_rect(center=button["position"])
                self.screen.blit(text, text_rect)

                
                if i == self.selected_button:
                    pygame.draw.rect(self.screen, (0, 0, 0), (text_rect.x - 8, text_rect.y - 8, text_rect.width + 16, text_rect.height + 16), 4)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main_menu = MainMenu((800, 600))
    main_menu.run()