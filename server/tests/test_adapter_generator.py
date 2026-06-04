from typing import Protocol

from server.src.generators import AdapterGenerator
from server.src.interfaces import IMovable
from server.src.ioc import Ioc
from server.src.scopes import InitCommand
from server.src.utils import Point, Vector


class TestInterface(Protocol):
    def get_location(self) -> Point:
        ...

    def set_location(self, p: Point) -> None:
        ...

    def get_velocity(self) -> Vector:
        ...

    def destroy(self) -> None:
        ...


class SpaceShip:
    def __init__(self, location: Point, velocity: Vector):
        self.location = location
        self.velocity = velocity

    def get_location(self):
        return self.location

    def set_location(self, p: Point):
        self.location = p

    def get_velocity(self):
        return self.velocity

    def destroy(self):
        self.location = None
        self.velocity = None


def create_test_space_ship() -> SpaceShip:
    p = Point(12, 5)
    v = Vector(-7, 3)
    return SpaceShip(location=p, velocity=v)


space_ship = create_test_space_ship()


class SetLocationCommand:
    def __init__(self, location: Point):
        self.location = location

    def execute(self):
        space_ship.set_location(self.location)


class DestroyCommand:
    def __init__(self):
        pass

    def execute(self):
        space_ship.destroy()


def init() -> None:
    InitCommand().execute()
    Ioc.resolve("IoC.Register", "Adapter",
                lambda interface, obj:                         # pylint: disable=W0108
                AdapterGenerator.generate_adapter(interface, obj)).execute()


def register_interface(t: type) -> None:
    def set_location(_adapter, location: Point, *args):        # pylint: disable=W0613
        return SetLocationCommand(location)
    def destroy(*args):                                        # pylint: disable=W0613
        return DestroyCommand()
    Ioc.resolve("IoC.Register", f"Spaceship.Operations.{t.__name__}.get_location",
                lambda: space_ship.get_location()).execute()   # pylint: disable=W0108
    Ioc.resolve("IoC.Register", f"Spaceship.Operations.{t.__name__}.set_location",
                set_location).execute()
    Ioc.resolve("IoC.Register", f"Spaceship.Operations.{t.__name__}.get_velocity",
                lambda: space_ship.get_velocity()).execute()   # pylint: disable=W0108
    if t.__name__ == "TestInterface":
        Ioc.resolve("IoC.Register", f"Spaceship.Operations.{t.__name__}.destroy",
                    destroy).execute()


def test_adapter_generator():
    init()
    register_interface(IMovable)
    adapter = Ioc.resolve("Adapter", IMovable, space_ship)
    assert adapter.get_location() == Point(12, 5)
    assert adapter.get_velocity() == Vector(-7, 3)
    adapter.set_location(Point(2, 2))
    assert adapter.get_location() == Point(2, 2)
    register_interface(TestInterface)
    adapter = Ioc.resolve("Adapter", TestInterface, space_ship)
    assert adapter.get_location() == Point(2, 2)
    assert adapter.get_velocity() == Vector(-7, 3)
    adapter.set_location(Point(3, 3))
    assert adapter.get_location() == Point(3, 3)
    adapter.destroy()
    assert adapter.get_location() is None
    assert adapter.get_velocity() is None
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
