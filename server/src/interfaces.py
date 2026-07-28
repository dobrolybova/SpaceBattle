from abc import ABC, abstractmethod
from typing import Protocol, Any

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


class IDirectionChangeable(Protocol):
    def get_velocity(self) -> int:
        ...

    def set_velocity(self, v: int) -> None:
        ...


class ICommand(Protocol):
    def execute(self):
        ...


class IExceptionHandler(Protocol):
    def handle(self, cmd: ICommand, exc: Exception) -> ICommand:
        ...


class IFuelConsumer(Protocol):
    def get_fuel_level(self) -> int:
        ...

    def set_fuel_level(self, level: int) -> None:
        ...

    def get_fuel_consumption_rate(self) -> int:
        ...


class IDependencyResolver(Protocol):
    def resolve(self, dependency: str, *args) -> Any:
        ...


class IThreadState(Protocol):
    def handle_command(self):
        ...

    def cur_queue(self):
        ...


class Obj(Protocol):
    def get_id(self) -> Any:
        ...


class Handler(ABC):
    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def execute(self, request: Any):
        ...


class NeighborhoodSystem(Protocol):
    def update_neighborhood(self, obj: IMovable | Obj) -> None:
        ...

    def define_neighborhood(self, obj: IMovable | Obj) -> int:
        ...

    def delete_obj_from_neighborhood(self, obj: IMovable | Obj) -> None:
        ...
