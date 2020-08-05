class Entity:
    _x = 0
    _y = 0

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def move(self, move_x, move_y):
        self._x += move_x
        self._y += move_y
        return

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y


class Paddle(Entity):
    HEIGHT = 1000
    WIDTH = 150
    MIDDLE_REGION = 200

    def __init__(self, x, y):
        super().__init__(x, y)


class Ball(Entity):
    BASE_MOVE_SPEED = 2.5
    RADIUS = 200

    _radius = 0
    _direction = 0
    _velocity = (0, 0)
    _move_speed = BASE_MOVE_SPEED

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self):
        self.move(self._velocity[0], self._velocity[1])
        return

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity
        return

    def set_direction(self, direction):
        self._direction = direction
        return
