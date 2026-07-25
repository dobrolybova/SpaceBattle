import pathlib
from collections import deque
from time import sleep

from server.src.interfaces import ICommand
from server.src.server_process_state import ServerThread, HardStop, NormalState, MoveToState, MoveToCommand, RunCommand

TEST_FLAG = False

class TestCommand:
    def __init__(self, cmd: ICommand = None, exc: Exception = None):  # pylint: disable=W0613
        self.msg = "test command is performed"
        self.path = f"{pathlib.Path().resolve()}.log"

    def execute(self):
        global TEST_FLAG           # pylint: disable=W0603
        TEST_FLAG = True


def test_server_hard_stop_normal_state():
    global TEST_FLAG
    assert not TEST_FLAG
    test_cmd = TestCommand()
    queue = deque()
    t = ServerThread(state=NormalState(q=queue))
    queue.append(test_cmd)
    shut_down_cmd = HardStop(server=t)
    queue.appendleft(shut_down_cmd)
    t.start_thread()
    assert t.thread.is_alive()
    assert TEST_FLAG
    count = 0
    while t.thread.is_alive():
        sleep(0.1)
        count += 1
        if count > 30:
            break
    assert not t.thread.is_alive()


def test_server_hard_stop_move_state():
    global TEST_FLAG
    TEST_FLAG = False
    assert not TEST_FLAG
    test_cmd = TestCommand()
    queue = deque()
    target_q = deque()
    t = ServerThread(state=MoveToState(q=queue, target_q=target_q))
    queue.append(test_cmd)
    shut_down_cmd = HardStop(server=t)
    queue.appendleft(shut_down_cmd)
    assert len(target_q) == 0
    t.start_thread()
    assert t.thread.is_alive()
    assert not TEST_FLAG
    count = 0
    while t.thread.is_alive():
        sleep(0.1)
        count += 1
        if count > 30:
            break
    assert not t.thread.is_alive()
    assert len(target_q) != 0


def test_server_switch_normal_to_move():
    global TEST_FLAG
    TEST_FLAG = False
    test_cmd = TestCommand()
    queue = deque()
    target_q = deque()
    t = ServerThread(state=NormalState(q=queue))
    assert isinstance(t.state, NormalState)
    queue.append(test_cmd)
    t.start_thread()
    assert t.thread.is_alive()
    assert TEST_FLAG
    TEST_FLAG = False
    move_cmd = MoveToCommand(server=t, target_q=target_q)
    assert len(target_q) == 0
    queue.append(test_cmd)
    queue.append(move_cmd)
    sleep(1)
    assert isinstance(t.state, MoveToState)
    assert not TEST_FLAG
    assert len(target_q) != 0
    t.stop_thread()
    assert not t.thread.is_alive()


def test_server_switch_move_to_normal():
    global TEST_FLAG
    TEST_FLAG = False
    test_cmd = TestCommand()
    queue = deque()
    target_q = deque()
    assert len(target_q) == 0
    t = ServerThread(state=MoveToState(q=queue, target_q=target_q))
    assert isinstance(t.state, MoveToState)
    queue.append(test_cmd)
    t.start_thread()
    assert t.thread.is_alive()
    assert not TEST_FLAG
    assert len(target_q) != 0
    run_cmd = RunCommand(server=t)
    queue.append(test_cmd)
    queue.append(run_cmd)
    sleep(1)
    assert isinstance(t.state, NormalState)
    assert TEST_FLAG
    t.stop_thread()
    assert not t.thread.is_alive()
