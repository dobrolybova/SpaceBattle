from server.src.commands import MacroCommand
from server.src.exceptions import FuelNotEnough
from server.src.interfaces import IMovable, IRotatable, IFuelConsumer, IDirectionChangeable
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


class CheckFuel:
    def __init__(self, fuel_consumer: IFuelConsumer):
        self.fuel_consumer = fuel_consumer

    def execute(self):
        if self.fuel_consumer.get_fuel_level() <= 0:
            raise FuelNotEnough()


class BurnFuel:
    def __init__(self, fuel_consumer: IFuelConsumer):
        self.fuel_consumer = fuel_consumer

    def execute(self):
        consumption_rate = self.fuel_consumer.get_fuel_consumption_rate()
        level = self.fuel_consumer.get_fuel_level()
        self.fuel_consumer.set_fuel_level(level=level - consumption_rate)


class ChangeVelocity:
    def __init__(self, direction_changeable: IDirectionChangeable, modifier: int):
        self.direction_changeable = direction_changeable
        self.modifier = modifier

    def execute(self):
        velocity = self.direction_changeable.get_velocity()
        self.direction_changeable.set_velocity(velocity + self.modifier)


class MoveWithChangeFuel(MacroCommand):
    def __init__(self, fuel_consumer: IFuelConsumer, movable: IMovable):
        super().__init__(commands = [
            CheckFuel(fuel_consumer=fuel_consumer),
            Move(movable=movable),
            BurnFuel(fuel_consumer=fuel_consumer)
        ])


class RotateWithChangeVelocity(MacroCommand):
    def __init__(self, rotatable: IRotatable, direction_changeable: IDirectionChangeable, modifier: int):
        super().__init__(commands=[
            Rotate(rotatable=rotatable),
            ChangeVelocity(direction_changeable=direction_changeable, modifier=modifier)
        ])
