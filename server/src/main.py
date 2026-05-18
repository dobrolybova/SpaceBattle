from collections import deque
from typing import List

from server.src.interfaces import ICommand, IExceptionHandler


def execute(queue, handlers: List[IExceptionHandler]) -> None:
    if len(queue) == 0:
        return
    cmd: ICommand = queue.pop()
    try:
        cmd.execute()
    except Exception as exc:
        for handler in handlers:
            recovery_cmd = handler.handle(cmd=cmd, exc=exc)
            if recovery_cmd:
                queue.append(recovery_cmd)
                break


def main_loop() -> None:
    queue = deque()
    handlers : List[IExceptionHandler] = []
    while True:
        execute(queue=queue, handlers=handlers)
