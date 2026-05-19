import pathlib
from typing import List

from server.src.interfaces import ICommand


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
