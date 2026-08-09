import pytest

from server.src.exceptions import ArgumentException, NoParentException
from server.src.interfaces import Obj
from server.src.ioc import Ioc
from server.src.movement import Move
from server.src.schemas import Order
from server.src.scopes import InitCommand
from server.src.utils import Point, Vector


class SpaceShip:   # pylint: disable=R0801
    def __init__(self, location: Point, velocity: Vector):
        self.location = location
        self.velocity = velocity

    def get_location(self):
        return self.location

    def set_location(self, p: Point):
        self.location = p

    def get_velocity(self):
        return self.velocity


class ScopeTestCommand:
    def __init__(self, obj: Obj):
        self.obj = obj


    def execute(self):
        # No logic, just to check function was called
        return self.obj


def get_obj_by_id(_id: int):
        return SpaceShip(location=Point(10, 4), velocity=Vector(1, 1))


def init() -> None:
    InitCommand().execute()
    ioc_scope = Ioc.resolve("IoC.Scope.Create")
    Ioc.resolve("IoC.Scope.Current.Set", ioc_scope).execute()


def test_register_no_parent():
    InitCommand().execute()
    with pytest.raises(NoParentException):
        Ioc.resolve("IoC.Scope.Parent")


def test_register():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    Ioc.resolve("IoC.Register", "someDependency", lambda : 1).execute()
    assert Ioc.resolve("someDependency") == 1


def test_register_exception():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    with pytest.raises(ArgumentException):
        Ioc.resolve("someDependency")


def test_parent_scope():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    Ioc.resolve("IoC.Register", "someDependency", lambda: 1).execute()
    _parent_scope = Ioc.resolve("IoC.Scope.Current")
    new_scope = Ioc.resolve("IoC.Scope.Create")
    Ioc.resolve("IoC.Scope.Current.Set", new_scope).execute()
    assert Ioc.resolve("someDependency") == 1
    assert Ioc.resolve("IoC.Scope.Current") == new_scope


def test_scope_in_scope():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    scope1 = Ioc.resolve("IoC.Scope.Create")
    scope2 = Ioc.resolve("IoC.Scope.Create", scope1)
    Ioc.resolve("IoC.Scope.Current.Set", scope1).execute()
    Ioc.resolve("IoC.Register", "someDependency", lambda: 1).execute()
    Ioc.resolve("IoC.Scope.Current.Set", scope2).execute()
    assert Ioc.resolve("someDependency") == 1


def test_players_in_scope():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    order = Order(id=1, action="ScopeTestCommand")
    obj = get_obj_by_id(order.id)
    cur_scope = Ioc.resolve("IoC.Scope.Current")
    assert "ScopeTestCommand" not in str(cur_scope)
    with pytest.raises(NoParentException):
        Ioc.resolve(order.action, obj).execute()
    new_scope = Ioc.resolve("IoC.Scope.Create")
    Ioc.resolve("IoC.Scope.Current.Set", new_scope).execute()
    Ioc.resolve("IoC.Register", order.action, lambda obj: ScopeTestCommand(obj=obj)).execute()
    new_cur_scope = Ioc.resolve("IoC.Scope.Current")
    assert "ScopeTestCommand" in str(new_cur_scope)
    Ioc.resolve(order.action, obj).execute()
