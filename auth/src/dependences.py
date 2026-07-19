from fastapi import HTTPException
from auth.src.schemas import GameData
from auth.src.utils import participants


def validate(item: GameData) -> GameData:
    if item.game_name not in participants.keys():  # pylint: disable=C0201
        raise HTTPException(status_code=400, detail=f"Game {item.game_name} not exists")
    if item.user_name not in participants.get(item.game_name, []):
        raise HTTPException(status_code=400, detail=f"Player {item.user_name} not in game {item.game_name}")
    return item
