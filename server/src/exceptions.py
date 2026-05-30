class FuelNotEnough(Exception):
    def __init__(self):
        pass

class ArgumentException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NoParentException(Exception):
    def __init__(self):
        pass
