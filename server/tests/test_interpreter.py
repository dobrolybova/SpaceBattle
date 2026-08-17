import pytest

from server.src.exceptions import NoParentException
from server.src.interfaces import Obj
from server.src.ioc import Ioc
from server.src.movement import Move, Stop, Fire
from server.src.schemas import Order
from server.src.scopes import InitCommand
from server.src.utils import Point, Vector


class SpaceShip:   # pylint: disable=R0801
    def __init__(self, location: Point, velocity: Vector, id: int):
        self.location = location
        self.velocity = velocity
        self.id = id

    def get_location(self):
        return self.location

    def set_location(self, p: Point):
        self.location = p

    def get_velocity(self):
        return self.velocity

    def get_id(self):
        return self.id


class TestObj:
    def __init__(self, id: int):
        self.id = id

    def get_id(self):
        return self.id


class TestCommand:
    def __init__(self, obj: Obj, arg: int):
        self.obj = obj
        self.arg = arg

    def execute(self):
        # No logic, just to check function was called
        return self.arg


def get_obj_by_id(id: int):
    # logic is strange, just for testing
    if 1<= id <= 10:
        # This is game object
        return SpaceShip(location=Point(10, 4), velocity=Vector(1, 1), id=id)
    # Non game abject
    return TestObj(id=id)


def init():
    InitCommand().execute()
    Ioc.resolve("IoC.Register", "Move", lambda obj: Move(movable=obj)).execute()
    Ioc.resolve("IoC.Register", "Stop", lambda obj: Stop(obj=obj)).execute()
    Ioc.resolve("IoC.Register", "Fire", lambda obj, velocity: Fire(obj=obj, velocity=velocity)).execute()
    Ioc.resolve("IoC.Register", "TestCommand", lambda obj, arg: TestCommand(obj=obj, arg=arg)).execute()


def test_orders():
    init()
    order = Order(id=1, action="Move")
    obj = get_obj_by_id(order.id)
    Ioc.resolve(order.action, obj).execute()
    assert obj.get_location() == Point(11, 5)
    order = Order(id=2, action="Stop")
    obj = get_obj_by_id(order.id)
    res = Ioc.resolve(order.action, obj).execute()
    assert res == 2
    order = Order(id=3, action="Fire", velocity=5)
    obj = get_obj_by_id(order.id)
    res = Ioc.resolve(order.action, obj, order.velocity).execute()
    assert res == 3
    order = Order(id=15, action="TestCommand", arg=33)
    obj = get_obj_by_id(order.id)
    res = Ioc.resolve(order.action, obj, order.arg).execute()
    assert res == 33
    order = Order(id=3, action="Unknown")
    obj = get_obj_by_id(order.id)
    with pytest.raises(NoParentException):
        Ioc.resolve(order.action, obj).execute()
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
