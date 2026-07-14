from typing import Optional

from pydantic import BaseModel


class ResponseData(BaseModel):
    status: int
    json: Optional[dict] = {}
    text: Optional[str] = ""


class TokenBody(BaseModel):
    game_name: str
