from typing import Any

import pytest

from server.src.commands import DefineNeighbor, DeleteNeighbor, UpdateNeighbor, CollisionDetectionCommand
from server.src.exceptions import OutOfGrid, CollisionDetected
from server.src.interfaces import Handler
from server.src.neighborhood import SimpleNeighborhoodSystem, ComplexNeighborhoodSystem
from server.src.utils import Point, Vector


class SpaceShip:
    def __init__(self, location: Point, id: int, velocity: Vector = Vector(0, 0)):
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


class TestCmd(Handler):
    def execute(self, _request: Any):
        pass


def test_define_neighborhood():
    neighborhood = SimpleNeighborhoodSystem(10)
    cmd = DefineNeighbor(neighborhood_system=neighborhood)
    assert neighborhood.neighborhood == {1: [], 2: [], 3: [], 4: []}
    ship = SpaceShip(location=Point(2, 3), id=1)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 1
    ship = SpaceShip(location=Point(2, 7), id=2)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 3
    ship = SpaceShip(location=Point(7, 7), id=3)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 4
    ship = SpaceShip(location=Point(7, 2), id=4)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 2
    ship = SpaceShip(location=Point(0, 0), id=5)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 1
    ship = SpaceShip(location=Point(5, 5), id=6)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 4
    ship = SpaceShip(location=Point(10, 10), id=7)
    cmd.execute(request=ship)
    assert neighborhood.cur_neighbor_num == 4


def test_define_neighborhood_exc():
    neighborhood = SimpleNeighborhoodSystem(10)
    cmd = DefineNeighbor(neighborhood_system=neighborhood)
    ship = SpaceShip(location=Point(17, 3), id=1)
    with pytest.raises(OutOfGrid):
        cmd.execute(request=ship)
    ship = SpaceShip(location=Point(1, 17), id=1)
    with pytest.raises(OutOfGrid):
        cmd.execute(request=ship)
    ship = SpaceShip(location=Point(17, 17), id=1)
    with pytest.raises(OutOfGrid):
        cmd.execute(request=ship)
    ship = SpaceShip(location=Point(-17, -17), id=1)
    with pytest.raises(OutOfGrid):
        cmd.execute(request=ship)


def test_update_neighborhood():
    ship1 = SpaceShip(location=Point(2, 3), id=1)
    ship2 = SpaceShip(location=Point(7, 7), id=2)
    ship3 = SpaceShip(location=Point(-7, 7), id=4)
    neighborhood = SimpleNeighborhoodSystem(10)
    assert neighborhood.neighborhood == {1: [], 2: [], 3: [], 4: []}
    finish_cmd = TestCmd()
    cmd_update = UpdateNeighbor(neighborhood_system=neighborhood, successor=finish_cmd)
    cmd_del = DeleteNeighbor(neighborhood_system=neighborhood, successor=cmd_update)
    cmd_def = DefineNeighbor(neighborhood_system=neighborhood, successor=cmd_del)
    cmd_def.execute(ship1)
    assert len(neighborhood.neighborhood.get(1)) == 1
    assert len(neighborhood.neighborhood.get(2)) == 0
    assert len(neighborhood.neighborhood.get(3)) == 0
    assert len(neighborhood.neighborhood.get(4)) == 0
    cmd_def.execute(ship2)
    assert len(neighborhood.neighborhood.get(1)) == 1
    assert len(neighborhood.neighborhood.get(2)) == 0
    assert len(neighborhood.neighborhood.get(3)) == 0
    assert len(neighborhood.neighborhood.get(4)) == 1
    ship1.set_location(Point(7, 7))
    cmd_def.execute(ship1)
    assert len(neighborhood.neighborhood.get(1)) == 0
    assert len(neighborhood.neighborhood.get(2)) == 0
    assert len(neighborhood.neighborhood.get(3)) == 0
    assert len(neighborhood.neighborhood.get(4)) == 2
    with pytest.raises(OutOfGrid):
        cmd_def.execute(request=ship3)


def test_update_complex_neighborhood():
    ship1 = SpaceShip(location=Point(1, 1), id=1)
    ship2 = SpaceShip(location=Point(3, 1), id=2)
    ship3 = SpaceShip(location=Point(5, 1), id=3)
    ship4 = SpaceShip(location=Point(1, 3), id=4)
    ship5 = SpaceShip(location=Point(1, 5), id=5)
    ship6 = SpaceShip(location=Point(3, 3), id=6)
    ship7 = SpaceShip(location=Point(3, 5), id=7)
    ship8 = SpaceShip(location=Point(5, 3), id=8)
    ship9 = SpaceShip(location=Point(5, 5), id=9)
    ship10 = SpaceShip(location=Point(7, 7), id=10)
    neighborhood = ComplexNeighborhoodSystem(6)
    assert neighborhood.neighborhood == {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    finish_cmd = TestCmd()
    cmd_update = UpdateNeighbor(neighborhood_system=neighborhood, successor=finish_cmd)
    cmd_del = DeleteNeighbor(neighborhood_system=neighborhood, successor=cmd_update)
    cmd_def = DefineNeighbor(neighborhood_system=neighborhood, successor=cmd_del)
    cmd_def.execute(ship1)
    cmd_def.execute(ship2)
    cmd_def.execute(ship3)
    cmd_def.execute(ship4)
    cmd_def.execute(ship5)
    cmd_def.execute(ship6)
    cmd_def.execute(ship7)
    cmd_def.execute(ship8)
    cmd_def.execute(ship9)
    with pytest.raises(OutOfGrid):
        cmd_def.execute(ship10)
    assert len(neighborhood.neighborhood.get(1)) == 1
    assert len(neighborhood.neighborhood.get(2)) == 1
    assert len(neighborhood.neighborhood.get(3)) == 1
    assert len(neighborhood.neighborhood.get(4)) == 1
    assert len(neighborhood.neighborhood.get(5)) == 1
    assert len(neighborhood.neighborhood.get(6)) == 1
    assert len(neighborhood.neighborhood.get(7)) == 1
    assert len(neighborhood.neighborhood.get(8)) == 1
    assert len(neighborhood.neighborhood.get(9)) == 1
    ship1.set_location(Point(5, 5))
    cmd_def.execute(ship1)
    assert len(neighborhood.neighborhood.get(1)) == 0
    assert len(neighborhood.neighborhood.get(2)) == 1
    assert len(neighborhood.neighborhood.get(3)) == 1
    assert len(neighborhood.neighborhood.get(4)) == 1
    assert len(neighborhood.neighborhood.get(5)) == 1
    assert len(neighborhood.neighborhood.get(6)) == 1
    assert len(neighborhood.neighborhood.get(7)) == 1
    assert len(neighborhood.neighborhood.get(8)) == 1
    assert len(neighborhood.neighborhood.get(9)) == 2


def test_collision_detection_empty_field_no_collision():
    neighborhood = SimpleNeighborhoodSystem(10)
    ship1 = SpaceShip(location=Point(2, 3), id=1)
    cmd = CollisionDetectionCommand(neighborhood_system=neighborhood)
    cmd.execute(ship1)


def test_collision_detection_diff_neighborhood_no_collision():
    neighborhood = SimpleNeighborhoodSystem(10)
    ship1 = SpaceShip(location=Point(2, 3), id=1)
    ship2 = SpaceShip(location=Point(7, 7), id=2)
    cmd_update = UpdateNeighbor(neighborhood_system=neighborhood)
    cmd_def = DefineNeighbor(neighborhood_system=neighborhood, successor=cmd_update)
    detection_cmd = CollisionDetectionCommand(neighborhood_system=neighborhood)
    cmd_def.execute(ship1)
    detection_cmd.execute(ship2)


def test_collision_detection_same_neighborhood_no_collision():
    neighborhood = SimpleNeighborhoodSystem(10)
    ship1 = SpaceShip(location=Point(2, 2), id=1)
    ship2 = SpaceShip(location=Point(0, 4), id=2)
    cmd_update = UpdateNeighbor(neighborhood_system=neighborhood)
    cmd_def = DefineNeighbor(neighborhood_system=neighborhood, successor=cmd_update)
    detection_cmd = CollisionDetectionCommand(neighborhood_system=neighborhood)
    cmd_def.execute(ship1)
    detection_cmd.execute(ship2)


def test_collision_detected():
    neighborhood = SimpleNeighborhoodSystem(10)
    ship1 = SpaceShip(location=Point(2, 3), id=1)
    ship2 = SpaceShip(location=Point(2, 3), id=2)
    cmd_update = UpdateNeighbor(neighborhood_system=neighborhood)
    cmd_def = DefineNeighbor(neighborhood_system=neighborhood, successor=cmd_update)
    detection_cmd = CollisionDetectionCommand(neighborhood_system=neighborhood)
    cmd_def.execute(ship1)
    with pytest.raises(CollisionDetected):
        detection_cmd.execute(ship2)


def test_collision_detection_only_with_two_neighborhoods():
    neighborhood1 = SimpleNeighborhoodSystem(12)
    neighborhood2 = ComplexNeighborhoodSystem(12)
    ship1 = SpaceShip(location=Point(5, 1), id=1)
    ship2 = SpaceShip(location=Point(6, 1), id=2)
    cmd_update1 = UpdateNeighbor(neighborhood_system=neighborhood1)
    cmd_def1 = DefineNeighbor(neighborhood_system=neighborhood1, successor=cmd_update1)
    cmd_update2 = UpdateNeighbor(neighborhood_system=neighborhood2)
    cmd_def2 = DefineNeighbor(neighborhood_system=neighborhood2, successor=cmd_update2)
    cmd_def1.execute(ship1)
    cmd_def2.execute(ship1)
    detection_cmd1 = CollisionDetectionCommand(neighborhood_system=neighborhood1)
    detection_cmd1.execute(ship2)
    detection_cmd2 = CollisionDetectionCommand(neighborhood_system=neighborhood2, successor=detection_cmd1)
    with pytest.raises(CollisionDetected):
        detection_cmd2.execute(ship2)
