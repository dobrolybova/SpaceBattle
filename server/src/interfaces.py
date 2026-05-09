from typing import Protocol

from server.src.utils import Point, Vector, Direction


class IMovable(Protocol):
    def get_location(self) -> Point:
        ...

    def set_location(self, p: Point) -> None:
        ...

    def get_velocity(self) -> Vector:
        ...


class IRotatable(Protocol):
    def get_direction(self) -> Direction:
        ...

    def set_direction(self, d: Direction) -> None:
        ...

    def get_angular_velocity(self) -> int:
        ...
