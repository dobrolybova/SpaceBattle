from server.src.interfaces import IMovable


class FuelNotEnough(Exception):
    def __init__(self):
        pass

class ArgumentException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NoParentException(Exception):
    def __init__(self):
        pass


class OutOfGrid(Exception):
    def __init__(self, obj: IMovable):
        self.obj = obj


class CollisionDetected(Exception):
    def __init__(self, obj1: IMovable, obj2: IMovable):
        self.obj1 = obj1
        self.obj2 = obj2
