from unittest.mock import patch

import pytest

from server.src.exceptions import FuelNotEnough
from server.src.movement import CheckFuel, BurnFuel
from server.tests.conftest import TestException


class FuelConsumer:
    def __init__(self, level: int, consumption_rate: int):
        self.level = level
        self.consumption_rate = consumption_rate

    def get_fuel_level(self) -> int:
        return self.level

    def set_fuel_level(self, level: int) -> None:
        self.level = level

    def get_fuel_consumption_rate(self) -> int:
        return self.consumption_rate


def test_check_fuel():
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    CheckFuel(fuel_consumer=fuel_consumer).execute()
    assert fuel_consumer.get_fuel_level() == fuel_level
    with pytest.raises(FuelNotEnough):
        fuel_level = 0
        fuel_consumer.set_fuel_level(level=fuel_level)
        CheckFuel(fuel_consumer=fuel_consumer).execute()
        fuel_level = - 5
        fuel_consumer.set_fuel_level(level=fuel_level)
        CheckFuel(fuel_consumer=fuel_consumer).execute()


@patch.object(FuelConsumer, "get_fuel_level", side_effect=TestException("Get fuel error"))
def test_check_fuel_get_fuel_exception(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    with pytest.raises(TestException) as exc:
        CheckFuel(fuel_consumer=fuel_consumer).execute()
    assert exc.value.get_msg() == "Get fuel error"


@patch.object(FuelConsumer, "set_fuel_level", side_effect=TestException("Set fuel error"))
def test_check_fuel_set_fuel_exception_not_raise(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    CheckFuel(fuel_consumer=fuel_consumer).execute()


@patch.object(FuelConsumer, "get_fuel_consumption_rate", side_effect=TestException("Get fuel consumption error"))
def test_check_fuel_get_fuel_consumption_rate_exception_not_raise(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    CheckFuel(fuel_consumer=fuel_consumer).execute()


def test_burn_fuel():
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    BurnFuel(fuel_consumer=fuel_consumer).execute()
    assert fuel_consumer.get_fuel_level() == 2
    BurnFuel(fuel_consumer=fuel_consumer).execute()
    assert fuel_consumer.get_fuel_level() == -1


@patch.object(FuelConsumer, "get_fuel_level", side_effect=TestException("Get fuel error"))
def test_burn_fuel_get_fuel_exception(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    with pytest.raises(TestException) as exc:
        BurnFuel(fuel_consumer=fuel_consumer).execute()
    assert exc.value.get_msg() == "Get fuel error"


@patch.object(FuelConsumer, "set_fuel_level", side_effect=TestException("Set fuel error"))
def test_burn_fuel_set_fuel_exception(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    with pytest.raises(TestException) as exc:
        BurnFuel(fuel_consumer=fuel_consumer).execute()
    assert exc.value.get_msg() == "Set fuel error"


@patch.object(FuelConsumer, "get_fuel_consumption_rate", side_effect=TestException("Get fuel consumption error"))
def test_burn_fuel_get_fuel_consumption_rate_exception(_mock):
    fuel_level = 5
    fuel_consumption_rate = 3
    fuel_consumer = FuelConsumer(level=fuel_level, consumption_rate=fuel_consumption_rate)
    with pytest.raises(TestException) as exc:
        BurnFuel(fuel_consumer=fuel_consumer).execute()
    assert exc.value.get_msg() == "Get fuel consumption error"
