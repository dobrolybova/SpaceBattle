from typing import Optional

from pydantic import BaseModel


class Participants(BaseModel):
    participants: list[str]


class GameData(BaseModel):
    game_name: str
    user_name: Optional[str] = ""


class JwtResp(BaseModel):
    jwt: str
