from unittest.mock import patch

import pytest

from server.src.movement import Rotate, ChangeVelocity, RotateWithChangeVelocity
from server.src.utils import Direction
from server.tests.conftest import TestException


class SpaceShip:
    def __init__(self, direction: Direction, angular_velocity: int):
        self.direction = direction
        self.angular_velocity = angular_velocity

    def get_direction(self):
        return self.direction

    def set_direction(self, d: Direction):
        self.direction = d

    def get_angular_velocity(self):
        return self.angular_velocity

    def get_velocity(self):
        return self.angular_velocity

    def set_velocity(self, angular_velocity: int):
        self.angular_velocity = angular_velocity



def create_test_space_ship() -> SpaceShip:
    direction = Direction(angle=45)
    angular_velocity = 45
    return SpaceShip(direction=direction, angular_velocity=angular_velocity)


def test_rotate():
    space_ship = create_test_space_ship()
    Rotate(space_ship).execute()
    assert space_ship.get_direction() == Direction(angle=90)


@patch.object(SpaceShip, "get_direction", side_effect=TestException("Get direction error"))
def test_rotate_get_direction_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Rotate(space_ship).execute()
    assert exc.value.get_msg() == "Get direction error"


@patch.object(SpaceShip, "set_direction", side_effect=TestException("Set direction error"))
def test_rotate_set_direction_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Rotate(space_ship).execute()
    assert exc.value.get_msg() == "Set direction error"


@patch.object(SpaceShip, "get_angular_velocity", side_effect=TestException("Get angular velocity error"))
def test_rotate_get_angular_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        Rotate(space_ship).execute()
    assert exc.value.get_msg() == "Get angular velocity error"


def test_change_velocity():
    space_ship = create_test_space_ship()
    ChangeVelocity(space_ship, 10).execute()
    assert space_ship.get_velocity() == 55


@patch.object(SpaceShip, "get_velocity", side_effect=TestException("Get velocity error"))
def test_change_velocity_get_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        ChangeVelocity(space_ship, 10).execute()
    assert exc.value.get_msg() == "Get velocity error"


@patch.object(SpaceShip, "set_velocity", side_effect=TestException("Set velocity error"))
def test_change_velocity_set_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        ChangeVelocity(space_ship, 10).execute()
    assert exc.value.get_msg() == "Set velocity error"


def test_rotate_with_change_velocity():
    space_ship = create_test_space_ship()
    RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert space_ship.get_velocity() == 55
    assert space_ship.get_angular_velocity() == 55
    assert space_ship.get_direction() == Direction(90)
    RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert space_ship.get_velocity() == 65
    assert space_ship.get_angular_velocity() == 65
    assert space_ship.get_direction() == Direction(145)


@patch.object(SpaceShip, "get_direction", side_effect=TestException("Get direction error"))
def test_rotate_with_change_velocity_get_direction_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert exc.value.get_msg() == "Get direction error"


@patch.object(SpaceShip, "set_direction", side_effect=TestException("Set direction error"))
def test_rotate_with_change_velocity_set_direction_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert exc.value.get_msg() == "Set direction error"


@patch.object(SpaceShip, "get_angular_velocity", side_effect=TestException("Get angular velocity error"))
def test_rotate_with_change_velocity_get_angular_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert exc.value.get_msg() == "Get angular velocity error"


@patch.object(SpaceShip, "get_velocity", side_effect=TestException("Get velocity error"))
def test_rotate_with_change_velocity_get_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert exc.value.get_msg() == "Get velocity error"


@patch.object(SpaceShip, "set_velocity", side_effect=TestException("Set velocity error"))
def test_rotate_with_change_velocity_set_velocity_error(_mock):
    space_ship = create_test_space_ship()
    with pytest.raises(TestException) as exc:
        RotateWithChangeVelocity(rotatable=space_ship, direction_changeable=space_ship, modifier=10).execute()
    assert exc.value.get_msg() == "Set velocity error"
