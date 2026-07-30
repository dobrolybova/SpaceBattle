import asyncio
import pathlib
from typing import List

from server.src.enums import OperationId
from server.src.exceptions import CollisionDetected
from server.src.interfaces import ICommand, IMovable, IRotatable, Handler, Obj, NeighborhoodSystem
from server.src.ioc import Ioc
from server.src.schemas import MoveArgs, RotateArgs


class WriteToLog:
    def __init__(self, exc: Exception, cmd: ICommand = None):  # pylint: disable=W0613
        self.exc = exc
        self.path = f"{pathlib.Path().resolve()}.log"

    def execute(self):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(repr(self.exc))


class RetryOnce:
    def __init__(self, cmd: ICommand, exc: Exception = None):  # pylint: disable=W0613
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()


class RetryTwice:
    def __init__(self, cmd: ICommand, exc: Exception = None):  # pylint: disable=W0613
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()


class MacroCommand:
    def __init__(self, commands: List[ICommand]):
        self.commands = commands

    def execute(self):
        for cmd in self.commands:
            cmd.execute()


class InterpretCommand:
    def __init__(self, object_id: IMovable | IRotatable, operation_id: OperationId, args: MoveArgs | RotateArgs):
        self.object_id = object_id
        self.operation_id = operation_id
        self.args = args

    async def execute(self):
        await asyncio.sleep(0)
        Ioc.resolve(self.operation_id, self.object_id).execute()


class DefineNeighbor(Handler):
    def __init__(self, neighborhood_system: NeighborhoodSystem, successor: Handler=None):
        super().__init__(successor)
        self.neighborhood_system = neighborhood_system

    def execute(self, request: IMovable):
        self.neighborhood_system.cur_neighbor_num = self.neighborhood_system.define_neighborhood(obj=request)
        if self._successor:
            self._successor.execute(request)


class DeleteNeighbor(Handler):
    def __init__(self, neighborhood_system: NeighborhoodSystem, successor: Handler=None):
        super().__init__(successor)
        self.neighborhood_system = neighborhood_system

    def execute(self, request: IMovable | Obj):
        if (self.neighborhood_system.obj_neighborhood.get(request.get_id()) and
                self.neighborhood_system.cur_neighbor_num !=
                self.neighborhood_system.obj_neighborhood.get(request.get_id())):
            self.neighborhood_system.delete_obj_from_neighborhood(obj=request)
        if self._successor:
            self._successor.execute(request)


class UpdateNeighbor(Handler):
    def __init__(self, neighborhood_system: NeighborhoodSystem, successor: Handler=None):
        super().__init__(successor)
        self.neighborhood_system = neighborhood_system

    def execute(self, request: IMovable):
        self.neighborhood_system.update_neighborhood(obj=request)
        if self._successor:
            self._successor.execute(request)


class CollisionCheckCommand:
    def __init__(self, obj1: IMovable, obj2: IMovable):
        self.obj1 = obj1
        self.obj2 = obj2

    def execute(self):
        # logic is wrong, use just for testing
        if (self.obj1.get_location().x + 1 == self.obj2.get_location().x or   # pylint: disable=R0916
            self.obj1.get_location().y + 1 == self.obj2.get_location().y or
            self.obj1.get_location().x - 1 == self.obj2.get_location().x or
            self.obj1.get_location().y - 1 == self.obj2.get_location().y or
            self.obj1.get_location().x == self.obj2.get_location().x or
            self.obj1.get_location().y == self.obj2.get_location().y
        ):
            raise CollisionDetected(obj1= self.obj1, obj2=self.obj2)


class CollisionCheckCommands(MacroCommand):
    def __init__(self, commands: list[ICommand]):
        super().__init__(commands=commands)


class CollisionDetectionCommand(Handler):
    def __init__(self, neighborhood_system: NeighborhoodSystem, successor: Handler=None):
        super().__init__(successor)
        self.neighborhood_system = neighborhood_system
        self.macro_cmd = {}

    def execute(self, request: IMovable | Obj):
        self.neighborhood_system.cur_neighbor_num = self.neighborhood_system.define_neighborhood(obj=request)
        neighbor_objs: list[IMovable] = (
            self.neighborhood_system.neighborhood.get(self.neighborhood_system.cur_neighbor_num))
        check_cmds = []
        for obj in neighbor_objs:
            check_cmds.append(CollisionCheckCommand(obj, request))
        macro_cmd = CollisionCheckCommands(check_cmds)
        self.macro_cmd.update({request.get_id(): macro_cmd})
        macro_cmd.execute()
