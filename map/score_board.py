from pygame.sprite import Sprite
import pygame
from sprites import X, Y, RED, GREEN, BLUE

HEIGHT = 100
POPUP_COUNTDOWN = 1000


class ScoreBoard(Sprite):
    def __init__(self, screen_dimensions, terrain, tank1, tank2):
        Sprite.__init__(self)

        # init stuff
        pygame.font.init()
        self._font = pygame.font.SysFont('Comic Sans MS', 20)

        # Passed in args
        self._dimensions = screen_dimensions
        self._terrain = terrain
        self._tank1 = tank1
        self._tank2 = tank2

        # Score board polygons
        self._scoreboard_outline = []
        self._ = []

        # Scoreboard text
        self._weapon_1_label = self._font.render('Weapon Type: ', False, RED)
        self._weapon_1_label_location = [2, 0]
        self._weapon_2_label = self._font.render('Weapon Type: ', False, RED)
        self._weapon_2_label_location = [self._dimensions[X]-200, 0]

        self._tank1_health = self._font.render('Tank 1 Health: ', False, BLUE)
        self._tank1_health_location = [2, 0]
        self._tank1_health_location[Y] = self._weapon_1_label_location[Y] + 20
        self._tank2_health = self._font.render('Tank 2 Health: ', False, RED)
        self._tank2_health_location = [self._weapon_2_label_location[X], 0]
        self._tank2_health_location[Y] = self._weapon_2_label_location[Y] + 20

        # Game over text
        self._game_over_label = self._font.render('Game over', False, RED)
        self._game_over_location = [self._dimensions[X]/2 - 150, self._dimensions[Y]/2]

        # Active player text
        self._active_player_label = self._font.render('Active player', False, RED)
        self._active_player_label_location = [self._dimensions[X]/2 - 150, self._dimensions[Y]/2]

        # Damage text
        self._damage_label = self._font.render('Damage', False, RED)
        self._damage_label_location = [self._dimensions[X]/2 - 150, 0]

        # Init the polygons and locations
        self._init_scoreboard()

        # State vars
        self._game_over = False
        self._active_player_countdown = 0
        self._damage_countdown = 0

    def update(self):
        self._weapon_1_label = self._font.render('Weapon: ' + self._tank1.get_current_weapon_name(), False, self._tank1.get_color())
        self._weapon_2_label = self._font.render('Weapon: ' + self._tank2.get_current_weapon_name(), False, self._tank2.get_color())

        self._tank1_health = self._font.render('Health: ' + str(self._tank1.get_health()), False, self._tank1.get_color())
        self._tank2_health = self._font.render('Health: ' + str(self._tank2.get_health()), False, self._tank2.get_color())

    def end_game(self, winner_tank):
        self._game_over = True
        self._game_over_label = self._font.render('Game over: ' + winner_tank.get_name() + " wins.", False, winner_tank.get_color())

    def damage_display(self, name, damage_amount):
        self._damage_label = self._font.render(name + ' damaged ' + str(damage_amount) + "!", False, RED)
        self._damage_countdown = POPUP_COUNTDOWN

    def switch_active_player(self, active_tank):
        self._active_player_label = self._font.render(active_tank.get_name() + "'s turn.", False, active_tank.get_color())
        self._active_player_countdown = POPUP_COUNTDOWN

    def draw(self, surface):
        # Draw game over if over
        if self._game_over:
            surface.blit(self._game_over_label, self._game_over_location)
        else:
            # Draw the outline
            pygame.draw.polygon(
                surface,
                GREEN,
                self._scoreboard_outline,
                2
            )

            # Draw weapon choice
            surface.blit(self._weapon_1_label, self._weapon_1_label_location)
            surface.blit(self._weapon_2_label, self._weapon_2_label_location)

            # Draw health
            surface.blit(self._tank1_health, self._tank1_health_location)
            surface.blit(self._tank2_health, self._tank2_health_location)

            # Display damage count down
            if self._damage_countdown > 0:
                surface.blit(self._damage_label, self._damage_label_location)
                self._damage_countdown -= 1

            # Display new active player text
            if self._active_player_countdown > 0:
                surface.blit(self._active_player_label, self._active_player_label_location)
                self._active_player_countdown -= 1

    def _init_scoreboard(self):

        # Draw the scoreboard
        self._scoreboard_outline = [
            [0, 0],  # UL
            [self._dimensions[X]-1, 0],  # UR
            [self._dimensions[X]-1, HEIGHT],  # LR
            [0, HEIGHT],  # LL
            [0, 0],  # UL - repeat first point to close the polygon
        ]
