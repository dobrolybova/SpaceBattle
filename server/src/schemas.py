from pydantic import BaseModel, ConfigDict

from server.src.enums import OperationId, GameStatus


class MoveArgs(BaseModel):
    pass


class RotateArgs(BaseModel):
    pass


class GameMessage(BaseModel):
    game_id: str
    object_id: str
    operation_id: OperationId
    args: MoveArgs | RotateArgs

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "game_id": "battle_001",
                    "object_id": "ship_001",
                    "operation_id": "movement",
                    "args": {},
                },
                {
                    "game_id": "battle_002",
                    "object_id": "ship_002",
                    "operation_id": "rotation",
                    "args": {}
                }
            ]
        }
    }


class GameResponse(BaseModel):
    game_status: GameStatus
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "game_status": "OK",
                    "message": "Команда успешно выполнена"
                }
            ]
        }
    }

class Order(BaseModel):
    id: int
    action: str
    model_config = ConfigDict(extra='allow')
