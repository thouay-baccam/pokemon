import pygame
import json
import os
from random import choice
from code.pokemon import Pokemon
from code.file_paths import (
    pokedex_path,
    save_path,
    pokemon_path,
    pkmnsprites_directory,
    backgrounds_directory,
    font_directory,
    music_directory,
)

class Combat:
    def __init__(self, player_pokemon_name):
        # `fmt` permet de dire à "black" (programme qui gère le format du code)
        # de ne pas toucher au tuple
        # fmt: off

        # Ce tuple est comme un tableau contenant
        # les facteurs par lesquels le dommage est multiplié
        # Basé sur le tableau Gen 2 de pokemondb.net/type
        self.type_chart = (
            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5),
            (0,1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2),
            (0,1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1),
            (0,1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1),
            (0,1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5),
            (0,1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5),
            (0,2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2),
            (0,1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0),
            (0,1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2),
            (0,1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5),
            (0,1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5),
            (0,1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5),
            (0,1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5),
            (0,0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5),
            (0,1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,0.5),
            (0,1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5)
        )
        # fmt: on
        pygame.init()
        # Sets up the game window with a specific size and title.
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Combat - Pokemon La Plateforme")

        self.clock = pygame.time.Clock()  # To control the frame rate

        # Loads the custom font
        self.custom_font_path = os.path.join(font_directory, "pkmn.ttf")
        self.font = pygame.font.Font(self.custom_font_path, 15)

        # Loads and scales the background image for the battle scene.
        self.background = pygame.image.load(
            os.path.join(backgrounds_directory, "battlebg.png")
        )
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Loads and plays the background music for the battle scene.
        pygame.mixer.music.load(os.path.join(music_directory, "battle.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Initializes game state variables
        self.is_running = True
        self.current_message = "A wild Pokémon appears!"
        self.player_pokemon = self.load_pokemon(player_pokemon_name)
        self.enemy_pokemon = self.load_random_pokemon()
        self.battle_state = 'START'

        # Defines rectangles for message and action boxes in the battle screen.
        self.message_box_rect = pygame.Rect(100, 500, 580, 90) 
        self.action_box_rect = pygame.Rect(600, 500, 190, 90) 

    def load_pokemon(self, pokemon_name):
        # Loads a specific Pokémon by name from the Pokémon data file.
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                if pokemon['name'] == pokemon_name:
                    return Pokemon(pokemon)
        raise ValueError(f"Pokémon with name {pokemon_name} not found.")


    def load_random_pokemon(self):
        # Loads a random Pokémon from the Pokémon data file for the enemy.
        with open(pokemon_path, "r") as file:
            pokemons = json.load(file)
            for pokemon in pokemons:
                pokemon["types"] = tuple(pokemon["types"])
            enemy_pokemon_data = choice(pokemons)
        return Pokemon(enemy_pokemon_data)
    
    def run(self):
        while self.is_running:
            self.handle_events()
            self.update_game_state()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

    def handle_mouse_click(self, event):
        if self.action_box_rect.collidepoint(event.pos):
            self.handle_action_click()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.render_pokemon_sprites()
        self.render_enemy_info()
        self.render_player_info()
        self.render_message_box()
        self.render_action_box(650, 480)
        
    def render_pokemon_sprites(self):
        # Renders the player's and enemy's Pokémon sprites on the battle screen.
        # Loads the sprites, scale them, and position them appropriately.
        player_pokemon_sprite = pygame.image.load(self.player_pokemon.back_sprite).convert_alpha()
        enemy_pokemon_sprite = pygame.image.load(self.enemy_pokemon.front_sprite).convert_alpha()

        desired_player_sprite_size = (200, 200)
        desired_enemy_sprite_size = (200, 200)

        player_scale_ratio = (desired_player_sprite_size[0] / player_pokemon_sprite.get_width(),
                            desired_player_sprite_size[1] / player_pokemon_sprite.get_height())
        enemy_scale_ratio = (desired_enemy_sprite_size[0] / enemy_pokemon_sprite.get_width(),
                            desired_enemy_sprite_size[1] / enemy_pokemon_sprite.get_height())

        player_pokemon_sprite = pygame.transform.scale(player_pokemon_sprite, desired_player_sprite_size)
        enemy_pokemon_sprite = pygame.transform.scale(enemy_pokemon_sprite, desired_enemy_sprite_size)

        player_sprite_anchor = (90, 447 - desired_player_sprite_size[1])
        enemy_sprite_anchor = (500, 70)

        self.screen.blit(player_pokemon_sprite, player_sprite_anchor)
        self.screen.blit(enemy_pokemon_sprite, enemy_sprite_anchor)

    def render_message_box(self):
        # Renders the message box on the battle screen to display game messages.
        lines = self.current_message.split('\n')
        start_y = self.message_box_rect.y + 10
        
        # Render each line
        for i, line in enumerate(lines):
            message_surface = self.font.render(line, True, (0, 0, 0))
            line_y = start_y + (i * 20)
            self.screen.blit(message_surface, (self.message_box_rect.x + 10, line_y))

    def render_enemy_info(self):
        # Renders the enemy Pokémon's name, health bar, and level on the screen.
        enemy_health_percent = self.get_health_percent(self.enemy_pokemon)
        enemy_name = self.enemy_pokemon.name
        enemy_level_text = f"Lvl {self.enemy_pokemon.level}"

        health_bar_surface = self.create_health_bar_surface(enemy_health_percent, (255, 0, 0))
        name_surface = self.font.render(enemy_name, True, (0, 0, 0))
        enemy_level_surface = self.font.render(enemy_level_text, True, (0, 0, 0))

        enemy_level_x = 130
        enemy_level_y = 98 

        self.screen.blit(name_surface, (100, 60))
        self.screen.blit(health_bar_surface, (128, 84))
        self.screen.blit(enemy_level_surface, (enemy_level_x, enemy_level_y))

    def render_player_info(self):
        # Render the player's Pokémon's name, health bar, and level on the screen.
        player_health_percent = self.get_health_percent(self.player_pokemon)
        player_name = self.player_pokemon.name
        player_level_text = f"Lvl {self.player_pokemon.level}"

        health_bar_surface = self.create_health_bar_surface(player_health_percent, (0, 255, 0))
        name_surface = self.font.render(player_name, True, (0, 0, 0))
        player_level_surface = self.font.render(player_level_text, True, (0, 0, 0))

        player_level_x = 656 
        player_level_y = 376 

        self.screen.blit(name_surface, (610, 338))
        self.screen.blit(health_bar_surface, (633, 362))  
        self.screen.blit(player_level_surface, (player_level_x, player_level_y))

    def create_health_bar_surface(self, health_percent, color):
        # Creates a surface for the health bar and fill it based on the Pokémon's health percentage.
        bar_width = 95
        bar_height = 6
        fill_width = int(bar_width * health_percent)

        health_bar_surface = pygame.Surface((bar_width, bar_height))
        health_bar_surface.fill((0, 0, 0))
        health_bar_surface.fill(color, (0, 0, fill_width, bar_height))

        return health_bar_surface

    def get_health_percent(self, pokemon):
        # Calculates the health percentage of a Pokémon based on its current health.
        health = min(pokemon.health, pokemon.max_health)
        return health / pokemon.max_health

    def render_action_box(self, pos_x, pos_y):
        # Renders the action box on the screen, which is used to proceed to the next action in the battle.
        action_text = "Next Action"

        action_surface = self.font.render(action_text, True, (0, 0, 0))
        text_width, text_height = action_surface.get_size()

        padding = 10 

        action_x = pos_x - (text_width // 2) - padding 
        action_y = pos_y - (text_height // 2) - padding
        action_width = text_width + 2 * padding
        action_height = text_height + 2 * padding
        action_rect = pygame.Rect(action_x, action_y, action_width, action_height)

        pygame.draw.rect(self.screen, (0, 255, 0), action_rect) 

        text_x = action_x + padding
        text_y = action_y + padding
        self.screen.blit(action_surface, (text_x, text_y))
        self.action_box_rect = action_rect

    def handle_action_click(self):
        # Handles clicks on the action box, updating the game state based on the current phase of the battle.
        if self.battle_state == 'START':
            self.battle_state = 'PLAYER_TURN'
        elif self.battle_state == 'PLAYER_TURN':
            # Performs player's attack
            self.perform_attack(self.player_pokemon, self.enemy_pokemon)
            if self.enemy_pokemon.health <= 0:
                self.battle_state = 'END'
                self.current_message = "The player's Pokemon has won!"
                self.player_pokemon.level_up()
            else:
                self.battle_state = 'ENEMY_TURN'
        elif self.battle_state == 'ENEMY_TURN':
            # Performs enemy's attack
            self.perform_attack(self.enemy_pokemon, self.player_pokemon)
            if self.player_pokemon.health <= 0:
                self.battle_state = 'END'
                self.current_message = "The player's Pokemon has lost!"
            else:
                self.battle_state = 'PLAYER_TURN'

    def update_game_state(self):
        # Placeholder
        pass

    def calculate_type_multiplier(self, attacker, defender):
         # Calculates the damage multiplier based on the types of the attacking and defending Pokémon.
        multipliers = [self.type_chart[attacker_type][defender_type]
                    for attacker_type in attacker.types
                    for defender_type in defender.types]
        return max(multipliers)

    def perform_attack(self, attacker, defender):
        # Perform an attack from one Pokémon to another, calculating damage, chance to miss and updating health.
        hit_chance = choice(range(0, 4))
        if hit_chance == 0:
            self.update_message_for_attack(attacker, defender, 0, missed=True)
            return
        
        multiplier = self.calculate_type_multiplier(attacker, defender)
        damage = int((attacker.attack / defender.defense) * multiplier * 10)
        defender.health -= max(damage, 1)  # Ensure minimum damage of 1

        self.update_message_for_attack(attacker, defender, multiplier)

    def calculate_damage(self, attacker, defender):
        # Where the calculations happen
        multipliers = []
        for attacker_type in attacker.types:
            for defender_type in defender.types:
                multipliers.append(self.type_chart[attacker_type][defender_type])
        multiplier = max(multipliers)

        damage = (attacker.attack / defender.defense) * multiplier * 10
        return max(int(damage), 1)  # Ensure minimum damage of 1

    def get_effectiveness(self, attacker, defender):
        #Placeholder
        return 1 

    def update_message_for_attack(self, attacker, defender, effectiveness, missed=False):
        # Updates the battle message based on the outcome of an attack.
        if missed:
            self.current_message = f"{attacker.name}'s attack missed!\n"
        else:
            attack_message = f"{attacker.name} attacks {defender.name}. "
            # Start with the attack message
            self.current_message = attack_message
            # Append the effectiveness message
            if effectiveness == 2:
                self.current_message += "\nIt's super effective!"
            elif effectiveness == 0.5:
                self.current_message += "\nIt's not very effective."
            elif effectiveness == 0:
                self.current_message += "\nIt had no effect!"
        # Add a new line for the next part of the message (so the thing isn't on the same line as the attack msg)
        self.current_message += "\n"
