from unittest.mock import patch

import pytest

from server.src.exceptions import FuelNotEnough
from server.src.movement import Move, MoveWithChangeFuel
from server.src.utils import Point, Vector
from server.tests.conftest import TestException


class SpaceShip:
    def __init__(self, location: Point, velocity: Vector, level: int, consumption_rate: int):
        self.location = location
        self.velocity = velocity
        self.level = level
        self.consumption_rate = consumption_rate

    def get_location(self):
        return self.location

    def set_location(self, p: Point):
        self.location = p

    def get_velocity(self):
        return self.velocity

    def get_fuel_level(self) -> int:
        return self.level

    def set_fuel_level(self, level: int) -> None:
        self.level = level

    def get_fuel_consumption_rate(self) -> int:
        return self.consumption_rate


def create_test_space_ship() -> SpaceShip:
    p = Point(12, 5)
    v = Vector(-7, 3)
    fuel_level = 5
    fuel_consumption_rate = 3
    return SpaceShip(location=p, velocity=v, level=fuel_level, consumption_rate=fuel_consumption_rate)


def test_move():
    space_ship = create_test_space_ship()
    Move(space_ship).execute()
    assert space_ship.get_location() == Point(5, 8)


@patch.object(SpaceShip, "get_location", side_effect=TestException("Get location error"))
def test_move_get_location_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Move(space_ship).execute()
    assert exc.value.get_msg() == "Get location error"


@patch.object(SpaceShip, "set_location", side_effect=TestException("Set location error"))
def test_move_set_location_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Move(space_ship).execute()
    assert exc.value.get_msg() == "Set location error"


@patch.object(SpaceShip, "get_velocity", side_effect=TestException("Get velocity error"))
def test_move_get_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Move(space_ship).execute()
    assert exc.value.get_msg() == "Get velocity error"


def test_move_with_change_fuel():
    space_ship = create_test_space_ship()
    MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert space_ship.get_location() == Point(5, 8)
    assert space_ship.get_fuel_level() == 2
    MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert space_ship.get_location() == Point(-2, 11)
    assert space_ship.get_fuel_level() == -1
    with pytest.raises(FuelNotEnough):
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()


@patch.object(SpaceShip, "get_location", side_effect=TestException("Get location error"))
def test_move_with_change_fuel_get_location_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Get location error"


@patch.object(SpaceShip, "set_location", side_effect=TestException("Set location error"))
def test_move_with_change_fuel_set_location_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Set location error"


@patch.object(SpaceShip, "get_velocity", side_effect=TestException("Get velocity error"))
def test_move_with_change_fuel_get_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Get velocity error"


@patch.object(SpaceShip, "get_fuel_level", side_effect=TestException("Get fuel error"))
def test_move_with_change_fuel_get_fuel_level_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Get fuel error"


@patch.object(SpaceShip, "set_fuel_level", side_effect=TestException("Set fuel error"))
def test_move_with_change_fuel_set_fuel_level_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Set fuel error"


@patch.object(SpaceShip, "get_fuel_consumption_rate", side_effect=TestException("Get fuel consumption error"))
def test_move_with_change_fuel_get_fuel_consumption_rate_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        MoveWithChangeFuel(fuel_consumer=space_ship, movable=space_ship).execute()
    assert exc.value.get_msg() == "Get fuel consumption error"
