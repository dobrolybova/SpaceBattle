import asyncio
import pathlib
from typing import List

from server.src.enums import OperationId
from server.src.interfaces import ICommand, IMovable, IRotatable
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
