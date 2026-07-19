from http import HTTPStatus
import jwt

from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from auth.src.schemas import GameData, JwtResp, Participants
from auth.src.dependences import validate

from auth.src.utils import update_participants

app = FastAPI()


@app.post("/api/v1/auth/token")
async def generate_jwt(item: GameData = Depends(validate)) ->JSONResponse:
    encoded_jwt = jwt.encode(
        {"game_name": item.game_name, "user_name": item.user_name}, 'secret', algorithm='HS256')
    return JSONResponse(status_code=HTTPStatus.OK, content=JwtResp(jwt=encoded_jwt).model_dump())


@app.post("/api/v1/auth/new_game")
async def create_new_game(item: Participants) -> GameData:
    new_game = update_participants(new_participants=item.participants)
    return GameData(game_name=new_game)
