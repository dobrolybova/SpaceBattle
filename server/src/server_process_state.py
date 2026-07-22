import threading
from collections import deque

from server.src.commands import WriteToLog
from server.src.interfaces import IThreadState, ICommand


class ServerThread:
    def __init__(self, state: IThreadState):
        self.state: IThreadState = state
        self.stop = threading.Event()

        def behaviour():
            state.handle_command()

        # pylint: disable=duplicate-code
        self.behaviour = behaviour

        def worker():
            while not self.stop.is_set():
                self.behaviour()

        self.thread = threading.Thread(target=worker)

    def start_thread(self):
        self.thread.start()

    def stop_thread(self):
        self.stop.set()
        self.thread.join()


class MoveToState:
    def __init__(self, q: deque, target_q: deque):
        self.q = q
        self.target_q = target_q

    def handle_command(self):
        try:
            cmd: ICommand = self.q.pop()
            if isinstance(cmd, (HardStop, RunCommand)):
                cmd.execute()
            else:
                self.target_q.append(cmd)
        except Exception as exc:
            WriteToLog(exc=exc).execute()

    def cur_queue(self):
        return self.target_q


class NormalState:
    def __init__(self, q: deque):
        self.q = q

    def handle_command(self):
        try:                       # pylint: disable=duplicate-code
            cmd: ICommand = self.q.pop()
            cmd.execute()
        except Exception as exc:
            WriteToLog(exc=exc).execute()

    def cur_queue(self):
        return self.q


class HardStop:
    def __init__(self, server: ServerThread):
        self.server = server

    def execute(self):
        self.server.stop_thread()


class MoveToCommand:
    def __init__(self, server: ServerThread, target_q: deque):
        self.server = server
        self.target_q = target_q

    def execute(self):
        q = self.server.state.cur_queue()
        state = MoveToState(q=q, target_q=self.target_q)
        self.server.state = state
        def behaviour():
            state.handle_command()
        self.server.behaviour = behaviour


class RunCommand:
    def __init__(self, server: ServerThread):
        self.server = server

    def execute(self):
        q = self.server.state.cur_queue()
        state = NormalState(q=q)
        self.server.state = state
        def behaviour():
            state.handle_command()
        self.server.behaviour = behaviour
