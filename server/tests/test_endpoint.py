from http import HTTPStatus

import pytest

from server.src.commands import InterpretCommand
from server.src.enums import OperationId, GameStatus
from server.src.ioc import Ioc
from server.src.movement import Move, Rotate
from server.src.scopes import InitCommand
from server.src.utils import Point, Vector, Direction


class SpaceShip:   # pylint: disable=R0801
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


objects_pool = {
    "battle_001": {
        "ship_001": SpaceShip(location=Point(12, 5), velocity=Vector(-7, 3), direction=Direction(angle=45),
                              angular_velocity=45),
        "ship_002": SpaceShip(location=Point(11, 5), velocity=Vector(7, 3), direction=Direction(angle=90),
                              angular_velocity=0),
        "ship_003": SpaceShip(location=Point(10, 5), velocity=Vector(-7, -3), direction=Direction(angle=0),
                              angular_velocity=90),
    },
    "battle_002": {
        "ship_010": SpaceShip(location=Point(12, 5), velocity=Vector(-7, 3), direction=Direction(angle=45),
                              angular_velocity=45),
        "ship_021": SpaceShip(location=Point(11, 5), velocity=Vector(7, 3), direction=Direction(angle=90),
                              angular_velocity=0),
        "ship_012": SpaceShip(location=Point(10, 5), velocity=Vector(-7, -3), direction=Direction(angle=0),
                              angular_velocity=90),
    },
}


def init():
    InitCommand().execute()
    Ioc.resolve("IoC.Register", "Get.Object",
                lambda game_id, object_id: objects_pool.get(game_id, {}).get(object_id)).execute()
    Ioc.resolve("IoC.Register", "InterpretCommand",
                lambda object_id, operation_id, args:
                InterpretCommand(object_id=object_id, operation_id=operation_id, args=args)).execute()
    Ioc.resolve("IoC.Register", "movement",
                lambda object_id: Move(movable=object_id)).execute()
    Ioc.resolve("IoC.Register", "rotation",
                lambda object_id: Rotate(rotatable=object_id)).execute()


def test_not_found(client):
    res = client.post("/find_person")
    assert res.json() == {'detail': 'Not Found'}
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_method_not_allowed(client):
    res = client.put("/api/v1/execute")
    assert res.json() == {'detail': 'Method Not Allowed'}
    assert res.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_unprocessable_entity(client):
    res = client.post(url="/api/v1/execute", json={})
    assert res.json() == {'detail': [{'input': {},
                         'loc': ['body', 'game_id'],
                         'msg': 'Field required',
                         'type': 'missing'},
                        {'input': {},
                         'loc': ['body', 'object_id'],
                         'msg': 'Field required',
                         'type': 'missing'},
                        {'input': {},
                         'loc': ['body', 'operation_id'],
                         'msg': 'Field required',
                         'type': 'missing'},
                        {'input': {},
                         'loc': ['body', 'args'],
                         'msg': 'Field required',
                         'type': 'missing'}]}
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_move(client):
    obj = objects_pool.get("battle_001").get("ship_001")
    assert obj.get_location() == Point(12, 5)
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    res = client.post(url="/api/v1/execute", json={
                                                    "game_id": "battle_001",
                                                    "object_id": "ship_001",
                                                    "operation_id": OperationId.MOVEMENT,
                                                    "args": {}
                                                })
    assert res.json() == {'game_status': GameStatus.OK, 'message': 'Команда успешно выполнена'}
    assert res.status_code == HTTPStatus.OK
    assert obj.get_location() == Point(5, 8)
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212


def test_rotate(client):
    obj = objects_pool.get("battle_001").get("ship_001")
    assert obj.get_direction() == Direction(45)
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    res = client.post(url="/api/v1/execute", json={
                                                    "game_id": "battle_001",
                                                    "object_id": "ship_001",
                                                    "operation_id": OperationId.ROTATION,
                                                    "args": {}
                                                })
    assert res.json() == {'game_status': GameStatus.OK, 'message': 'Команда успешно выполнена'}
    assert res.status_code == HTTPStatus.OK
    assert obj.get_direction() == Direction(90)
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212


@pytest.mark.parametrize(
    "game_id, object_id",
    [
        ("battle_005", "ship_001"),
        ("battle_001", "ship_005")
    ],
)
def test_no_game_or_obj(client, game_id, object_id):
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    res = client.post(url="/api/v1/execute", json={
                                                    "game_id": game_id,
                                                    "object_id": object_id,
                                                    "operation_id": OperationId.MOVEMENT,
                                                    "args": {}
                                                })
    assert res.json() == {
        'game_status': GameStatus.GAME_OR_OBJECT_NOT_FOUND,
        'message': f'Игра {game_id} не найдена или для нее не существует объекта {object_id}'
    }
    assert res.status_code == HTTPStatus.OK
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
