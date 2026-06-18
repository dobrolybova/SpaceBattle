from fastapi import FastAPI

from server.src.enums import GameStatus
from server.src.interfaces import IMovable, IRotatable
from server.src.ioc import Ioc
from server.src.schemas import GameMessage, GameResponse


app = FastAPI()


@app.post("/api/v1/execute")
async def update_item(item: GameMessage) -> GameResponse:
    obj: IMovable | IRotatable = Ioc.resolve("Get.Object", item.game_id, item.object_id)
    if not obj:
        return GameResponse(
            game_status=GameStatus.GAME_OR_OBJECT_NOT_FOUND,
            message=f"Игра {item.game_id} не найдена или для нее не существует объекта {item.object_id}"
        )
    await Ioc.resolve("InterpretCommand", obj, item.operation_id, item.args).execute()
    return GameResponse(game_status=GameStatus.OK, message="Команда успешно выполнена")
