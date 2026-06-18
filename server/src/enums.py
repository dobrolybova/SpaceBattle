from enum import Enum


class OperationId(str, Enum):
    MOVEMENT = 'movement'
    ROTATION = 'rotation'


class GameStatus(str, Enum):
    OK = "OK"
    GAME_OR_OBJECT_NOT_FOUND = "GAME_OR_OBJECT_NOT_FOUND"
