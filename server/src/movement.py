from server.src.interfaces import IMovable, IRotatable
from server.src.utils import Vector, Point, Direction


class Move:
    def __init__(self, movable: IMovable):
        self.movable = movable

    def execute(self):
        velocity: Vector = self.movable.get_velocity()
        location: Point = self.movable.get_location()
        self.movable.set_location(location.next(velocity))


class Rotate:
    def __init__(self, rotatable: IRotatable):
        self.rotatable = rotatable

    def execute(self):
        angular_velocity: int = self.rotatable.get_angular_velocity()
        direction: Direction = self.rotatable.get_direction()
        self.rotatable.set_direction(direction.next(angular_velocity))
