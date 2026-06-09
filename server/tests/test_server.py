import pathlib
from collections import deque
from time import sleep

from server.src.interfaces import ICommand
from server.src.server import ServerThread, HardStop, SoftStop
from server.tests.conftest import TestException

TEST_FLAG = False

class TestCommandExc:
    def __init__(self, cmd: ICommand = None, exc: Exception = None):  # pylint: disable=W0613
        pass

    def execute(self):
        raise TestException(msg="test command")


class TestCommand:
    def __init__(self, cmd: ICommand = None, exc: Exception = None):  # pylint: disable=W0613
        self.msg = "test command is performed"
        self.path = f"{pathlib.Path().resolve()}.log"

    def execute(self):
        global TEST_FLAG           # pylint: disable=W0603
        TEST_FLAG = True


def test_server_starts_and_performs_commands():
    assert not TEST_FLAG
    test_cmd = TestCommand()
    queue = deque()
    queue.append(test_cmd)
    t = ServerThread(q=queue)
    t.start_thread()
    assert t.thread.is_alive()
    t.stop_thread()
    assert TEST_FLAG
    assert not t.thread.is_alive()


def test_server_starts_and_performs_commands_exc():
    test_cmd = TestCommandExc()
    queue = deque()
    queue.append(test_cmd)
    t = ServerThread(q=queue)
    t.start_thread()
    assert t.thread.is_alive()
    t.stop_thread()
    assert not t.thread.is_alive()


def test_server_hard_stop():
    queue = deque()
    t = ServerThread(q=queue)
    test_cmd = TestCommand()
    queue.append(test_cmd)
    shut_down_cmd = HardStop(server=t)
    queue.append(shut_down_cmd)
    t.start_thread()
    assert t.thread.is_alive()
    count = 0
    while t.thread.is_alive():
        sleep(0.1)
        count += 1
        if count > 30:
            break
    assert not t.thread.is_alive()
    assert len(t.q) != 0


def test_server_soft_stop():
    queue = deque()
    t = ServerThread(q=queue)
    test_cmd = TestCommand()
    queue.append(test_cmd)
    shut_down_cmd = SoftStop(server=t)
    queue.append(shut_down_cmd)
    t.start_thread()
    assert t.thread.is_alive()
    count = 0
    while t.thread.is_alive():
        sleep(0.1)
        count += 1
        if count > 30:
            break
    assert not t.thread.is_alive()
    assert len(t.q) == 0
