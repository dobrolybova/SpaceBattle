import pathlib
from collections import deque
from typing import List
from unittest.mock import patch

from server.src.commands import RetryOnce, WriteToLog, RetryTwice
from server.src.handlers import RetryOnceThenLogHandler, RetryTwiceThenLogHandler, PutInQueueWriteToLogHandler, \
    PutInQueueRetryOnceHandler
from server.src.interfaces import IExceptionHandler
from server.src.main import execute
from server.src.movement import Move
from server.src.utils import Point, Vector, Direction
from server.tests.conftest import TestException


class SpaceShip:
    def __init__(self, location: Point, velocity: Vector, direction: Direction, angular_velocity: int):
        self.location = location
        self.velocity = velocity
        self.direction = direction
        self.angular_velocity = angular_velocity

    def get_location(self):
        return self.location

    def set_location(self, p: Point):
        self.location = p

    def get_velocity(self):
        return self.velocity

    def get_direction(self):
        return self.direction

    def set_direction(self, d: Direction):
        self.direction = d

    def get_angular_velocity(self):
        return self.angular_velocity


def create_test_space_ship() -> SpaceShip:
    p = Point(12, 5)
    v = Vector(-7, 3)
    direction = Direction(angle=45)
    angular_velocity = 45
    return SpaceShip(location=p, velocity=v, direction=direction, angular_velocity=angular_velocity)


def test_no_exceptions():
    move_cmd = Move(create_test_space_ship())
    queue = deque()
    queue.append(move_cmd)
    handlers: List[IExceptionHandler] = [
        PutInQueueWriteToLogHandler(),
        PutInQueueRetryOnceHandler(),
        RetryOnceThenLogHandler,
        RetryTwiceThenLogHandler
    ]
    execute(queue=queue, handlers=handlers)
    assert len(queue) == 0
    execute(queue=queue, handlers=handlers)


@patch.object(SpaceShip, "get_location", side_effect=TestException("error message"))
def test_put_in_queue_write_to_log(_mock, fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    move_cmd = Move(create_test_space_ship())
    queue = deque()
    queue.append(move_cmd)
    handlers: List[IExceptionHandler] = [PutInQueueWriteToLogHandler()]
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, WriteToLog)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    f = fs.get_object(file_path)
    assert f.contents == "error message"


@patch.object(SpaceShip, "get_location", side_effect=TestException("error message"))
def test_put_in_queue_retry_once(_mock):
    move_cmd = Move(create_test_space_ship())
    queue = deque()
    queue.append(move_cmd)
    handlers: List[IExceptionHandler] = [PutInQueueRetryOnceHandler()]
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, RetryOnce)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)


@patch.object(SpaceShip, "get_location", side_effect=TestException("error message"))
def test_retry_once(_mock, fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    move_cmd = Move(create_test_space_ship())
    queue = deque()
    queue.append(move_cmd)
    handlers : List[IExceptionHandler] = [RetryOnceThenLogHandler()]
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, RetryOnce)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, WriteToLog)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    f = fs.get_object(file_path)
    assert f.contents == "error message"


@patch.object(SpaceShip, "get_location", side_effect=TestException("error message"))
def test_retry_twice(_mock, fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    move_cmd = Move(create_test_space_ship())
    queue = deque()
    queue.append(move_cmd)
    handlers : List[IExceptionHandler] = [RetryTwiceThenLogHandler()]
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, RetryTwice)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, RetryOnce)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    queue_member = queue.pop()
    assert isinstance(queue_member, WriteToLog)
    queue.append(queue_member)
    execute(queue=queue, handlers=handlers)
    f = fs.get_object(file_path)
    assert f.contents == "error message"
