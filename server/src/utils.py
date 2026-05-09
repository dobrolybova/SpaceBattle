class Vector:
    def __init__(self, x: int, y: int):
        self.xx = x
        self.yy = y

    @property
    def x(self) -> int:
        return self.xx

    @property
    def y(self) -> int:
        return self.yy


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def next(self, v: Vector):
        self.x += v.x
        self.y += v.y
        return self

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y


class Direction:
    def __init__(self, angle: int):
        self.angle = angle

    def next(self, angular_velocity: int):
        self.angle += angular_velocity
        return self

    def __eq__(self, direction):
        return self.angle == direction.angle
