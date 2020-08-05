import pygame
import World
import Entity

from pygame.locals import *


class Renderer:
    # ============
    # Constants
    # ============
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    BORDER = 5

    HUD_Y = 100
    SCORE_Y = 20
    SCORE_X_P1 = 20
    SCORE_X_P2 = 924

    GREEN = (50, 225, 50)
    GREY = (128, 128, 128)

    # ============
    # Attributes
    # ============
    _screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    _world = None
    _paddle_height = 0
    _paddle_width = 0
    _ball_radius_x = 0
    _ball_radius_y = 0
    _font = None

    # ============
    # Functions
    # ============
    def __init__(self, world):
        self._world = world
        self._paddle_width = round((Renderer.SCREEN_WIDTH - (2 * Renderer.BORDER)) *
                                   (Entity.Paddle.WIDTH / World.World.WORLD_WIDTH))
        self._paddle_height = round((Renderer.SCREEN_HEIGHT - Renderer.HUD_Y - (3 * Renderer.BORDER)) *
                                    (Entity.Paddle.HEIGHT / World.World.WORLD_HEIGHT))
        self._ball_radius_x = round((Renderer.SCREEN_WIDTH - (2 * Renderer.BORDER)) *
                                   (Entity.Ball.RADIUS / World.World.WORLD_WIDTH))
        self._ball_radius_y = round((Renderer.SCREEN_HEIGHT - Renderer.HUD_Y - (3 * Renderer.BORDER)) *
                                    (Entity.Ball.RADIUS / World.World.WORLD_HEIGHT))
        pygame.font.init()
        self._font = pygame.font.SysFont('Consolas', 72)

    @staticmethod
    def world_to_screen(x, y):
        screen_xy = (((x / World.World.WORLD_WIDTH) * (Renderer.SCREEN_WIDTH - (2 * Renderer.BORDER))) +
                     Renderer.BORDER, ((y / World.World.WORLD_HEIGHT) * (Renderer.SCREEN_HEIGHT - Renderer.HUD_Y -
                                                                         (3 * Renderer.BORDER))) +
                     Renderer.HUD_Y + (2 * Renderer.BORDER))
        return screen_xy

    def draw(self):
        # Clear last frame
        self._screen.fill((0, 0, 0))

        # Draw new frame
        self.draw_title()
        self.draw_scores()
        self.draw_borders()
        self.draw_player(self._world.player1)
        self.draw_player(self._world.player2)
        self.draw_ball(self._world.ball)

        # Update display
        pygame.display.update()
        return

    def draw_borders(self):
        # HUD
        pygame.draw.rect(self._screen,
                         Renderer.GREY,
                         Rect((Renderer.BORDER / 2), (Renderer.BORDER / 2),
                              Renderer.SCREEN_WIDTH - Renderer.BORDER,
                              Renderer.HUD_Y + (Renderer.BORDER / 2)),
                         Renderer.BORDER)

        # World
        pygame.draw.rect(self._screen,
                         Renderer.GREY,
                         Rect((Renderer.BORDER / 2),
                              Renderer.HUD_Y + Renderer.BORDER,
                              Renderer.SCREEN_WIDTH - Renderer.BORDER,
                              Renderer.SCREEN_HEIGHT - Renderer.HUD_Y - Renderer.BORDER),
                         Renderer.BORDER)

    def draw_player(self, player):
        pos = Renderer.world_to_screen(player.get_paddle().get_x(), player.get_paddle().get_y())
        pygame.draw.rect(self._screen,
                         Renderer.GREEN,
                         Rect(round(pos[0]), round(pos[1]), self._paddle_width, self._paddle_height))
        return

    def draw_ball(self, ball):
        pos = Renderer.world_to_screen(ball.get_x(), ball.get_y())
        pygame.draw.ellipse(self._screen, Renderer.GREEN,
                            Rect(round(pos[0]), round(pos[1]), self._ball_radius_x, self._ball_radius_y))
        return

    def draw_scores(self):
        if self._world.player1.get_score() < 10:
            p1_score = self._font.render('0' + str(self._world.player1.get_score()), False, Renderer.GREEN)
        else:
            p1_score = self._font.render(str(self._world.player1.get_score()), False, Renderer.GREEN)

        if self._world.player2.get_score() < 10:
            p2_score = self._font.render('0' + str(self._world.player2.get_score()), False, Renderer.GREEN)
        else:
            p2_score = self._font.render(str(self._world.player2.get_score()), False, Renderer.GREEN)

        self._screen.blit(p1_score, (Renderer.SCORE_X_P1, Renderer.SCORE_Y))
        self._screen.blit(p2_score, (Renderer.SCORE_X_P2, Renderer.SCORE_Y))
        return

    def draw_title(self):
        text = self._font.render('PYPONG', False, Renderer.GREEN)
        self._screen.blit(text, (Renderer.SCREEN_WIDTH / 2 - 100, Renderer.SCORE_Y))
        return
