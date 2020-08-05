import random
import pygame
import Entity
import Controls


class Player:
    MOVE_SPEED = 7.5

    _score = 0
    _paddle = None
    _upKey = None
    _downKey = None
    _max_y = 0

    def __init__(self, world, paddle, up_key, down_key):
        self._paddle = paddle
        self._upKey = up_key
        self._downKey = down_key
        self._max_y = world.WORLD_HEIGHT - Entity.Paddle.HEIGHT

    def update(self, pressed_keys):
        if pressed_keys[self._upKey]:
            self._paddle.move(0, -1 * self.MOVE_SPEED)
            if self._paddle.get_y() < 0:
                self._paddle.set_y(0)

        if pressed_keys[self._downKey]:
            self._paddle.move(0, self.MOVE_SPEED)
            if self._paddle.get_y() > self._max_y:
                self._paddle.set_y(self._max_y)
        return

    def inc_score(self):
        self._score += 1
        return

    def get_score(self):
        return self._score

    def get_paddle(self):
        return self._paddle


class World:
    # ============
    # Constants
    # ============
    WORLD_WIDTH = 7000
    WORLD_HEIGHT = 5000

    PLAYER1_X = 100
    PLAYER2_X = WORLD_WIDTH - Entity.Paddle.WIDTH - 100

    BALL_SPEED_INC = 1.1
    BALL_SPEED_INC_TICKS = 1000

    # ============
    # Attributes
    # ============
    player1 = None
    player2 = None
    ball = None

    _tick = 0
    _game_paused = True
    _game_started = False

    # ============
    # Functions
    # ============
    def __init__(self):
        self.init_entities()
        return

    def init_entities(self):
        self.player1 = Player(self,
                              Entity.Paddle(World.PLAYER1_X, (World.WORLD_HEIGHT / 2) - (Entity.Paddle.HEIGHT / 2)),
                              Controls.PLAYER1_UP,
                              Controls.PLAYER1_DOWN)
        self.player2 = Player(self,
                              Entity.Paddle(World.PLAYER2_X, (World.WORLD_HEIGHT / 2) - (Entity.Paddle.HEIGHT / 2)),
                              Controls.PLAYER2_UP,
                              Controls.PLAYER2_DOWN)
        self.ball = Entity.Ball((World.WORLD_WIDTH / 2),
                                (World.WORLD_HEIGHT / 2))
        return

    def update(self):
        # Get input
        pressed_keys = pygame.key.get_pressed()

        if not self._game_paused:
            # Update players
            self.player1.update(pressed_keys)
            self.player2.update(pressed_keys)

            # Update ball
            self.ball.update()

            # Check collision
            self.check_collision_player(self.player1)
            self.check_collision_player(self.player2)
            # Colliding with side walls means score, hence reset
            if self.check_collision_walls():
                self.reset()

            # Check pause
            if pressed_keys[Controls.PAUSE]:
                self._game_paused = True

            # Update ticks
            self._tick += 1

            # Increase ball speed
            if self._tick > World.BALL_SPEED_INC_TICKS:
                self.ball.set_velocity((World.BALL_SPEED_INC * self.ball.get_velocity()[0],
                                        World.BALL_SPEED_INC * self.ball.get_velocity()[1]))
                self._tick = 0
        else:
            if pressed_keys[Controls.PAUSE]:
                self._game_paused = False

                if not self._game_started:
                    if random.random() > 0.5:
                        self.ball.set_velocity((Entity.Ball.BASE_MOVE_SPEED, 0))
                    else:
                        self.ball.set_velocity((-1 * Entity.Ball.BASE_MOVE_SPEED, 0))
                    self._game_started = True
        return

    def check_collision_player(self, player):
        collision = False

        if player.get_paddle().get_x() < self.ball.get_x() < (player.get_paddle().get_x() + Entity.Paddle.WIDTH) or \
                player.get_paddle().get_x() < (self.ball.get_x() + Entity.Ball.RADIUS) < \
                (player.get_paddle().get_x() + Entity.Paddle.WIDTH):

            # Top
            if (self.ball.get_y() + Entity.Ball.RADIUS) > player.get_paddle().get_y() and \
                    (self.ball.get_y() + (Entity.Ball.RADIUS / 2)) < \
                    (player.get_paddle().get_y() + (Entity.Paddle.HEIGHT / 2) - (Entity.Paddle.MIDDLE_REGION / 2)):
                if self.ball.get_velocity()[0] > 0:
                    self.ball.set_velocity((self.ball.get_velocity()[0] * -1, self.ball.get_velocity()[0] * -1))
                else:
                    self.ball.set_velocity((self.ball.get_velocity()[0] * -1, self.ball.get_velocity()[0]))
                collision = True
            # Bottom
            elif self.ball.get_y() < (player.get_paddle().get_y() + Entity.Paddle.HEIGHT) and \
                    (self.ball.get_y() + (Entity.Ball.RADIUS / 2)) > \
                    (player.get_paddle().get_y() + (Entity.Paddle.HEIGHT / 2) + (Entity.Paddle.MIDDLE_REGION / 2)):
                if self.ball.get_velocity()[0] > 0:
                    self.ball.set_velocity((self.ball.get_velocity()[0] * -1, self.ball.get_velocity()[0]))
                else:
                    self.ball.set_velocity((self.ball.get_velocity()[0] * -1, self.ball.get_velocity()[0] * -1))
                collision = True
            # Middle - if we reach here and we are inside bounds of paddle, middle hit
            elif self.ball.get_y() < (player.get_paddle().get_y() + Entity.Paddle.HEIGHT) and \
                    (self.ball.get_y() + Entity.Ball.RADIUS) > player.get_paddle().get_y():
                self.ball.set_velocity((self.ball.get_velocity()[0] * -1, self.ball.get_velocity()[1]))
                collision = True

            # If ball is embedded, remove it
            if collision:
                if player.get_paddle().get_x() < self.ball.get_x() < player.get_paddle().get_x() + Entity.Paddle.WIDTH:
                    self.ball.set_x(player.get_paddle().get_x() + Entity.Paddle.WIDTH + 1)
                elif player.get_paddle().get_x() < self.ball.get_x() + Entity.Ball.RADIUS < player.get_paddle().get_x() + \
                        Entity.Paddle.WIDTH:
                    self.ball.set_x(player.get_paddle().get_x() - Entity.Ball.RADIUS - 1)
        return

    def check_collision_walls(self):
        # Check for bounce
        if self.ball.get_y() <= 0 or self.ball.get_y() + Entity.Ball.RADIUS >= World.WORLD_HEIGHT:
            self.ball.set_velocity((self.ball.get_velocity()[0], self.ball.get_velocity()[1] * -1))
            return False

        # Check for scoring
        if self.ball.get_x() <= 0:
            self.player2.inc_score()
            return True
        elif self.ball.get_x() + Entity.Ball.RADIUS >= World.WORLD_WIDTH:
            self.player1.inc_score()
            return True

        return False

    def reset(self):
        self._game_paused = True
        self._game_started = False
        self._tick = 0
        self.player1.get_paddle().set_y((World.WORLD_HEIGHT / 2) - (Entity.Paddle.HEIGHT / 2))
        self.player2.get_paddle().set_y((World.WORLD_HEIGHT / 2) - (Entity.Paddle.HEIGHT / 2))
        self.ball.set_x((World.WORLD_WIDTH / 2) - (Entity.Ball.RADIUS / 2))
        self.ball.set_y((World.WORLD_HEIGHT / 2) - (Entity.Ball.RADIUS / 2))
        self.ball.set_velocity((0, 0))
        return
