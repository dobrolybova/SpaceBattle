from unittest.mock import patch

import pytest

from server.src.movement import Move
from server.src.utils import Point, Vector
from server.tests.conftest import TestException


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


def create_test_space_ship() -> SpaceShip:
    p = Point(12, 5)
    v = Vector(-7, 3)
    return SpaceShip(location=p, velocity=v)


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
