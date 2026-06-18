from collections import deque
import threading

from server.src.commands import WriteToLog
from server.src.interfaces import ICommand


class ServerThread:
    def __init__(self, q: deque):
        self.q = q
        self.stop = threading.Event()

        def behaviour():
            try:
                cmd: ICommand = self.q.pop()
                cmd.execute()
            except Exception as exc:
                WriteToLog(exc=exc).execute()

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


class HardStop:
    def __init__(self, server: ServerThread):
        self.server = server

    def execute(self):
        self.server.stop_thread()


class SoftStop:
    def __init__(self, server: ServerThread):
        self.server = server

    def execute(self):
        if len(self.server.q) == 0:
            self.server.stop_thread()
        else:
            self.server.q.appendleft(self)
