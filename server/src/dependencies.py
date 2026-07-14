import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from server.src.schemas import GameMessage

security = HTTPBearer()

def has_access(item: GameMessage, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    game_name = payload.get("game_name")
    if game_name != item.game_id:
        raise HTTPException(status_code=401, detail=f"Wrong game name {game_name} in token")
