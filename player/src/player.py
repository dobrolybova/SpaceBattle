from player.src.requester import Requester
from player.src.schemas import ResponseData, TokenBody
from server.src.schemas import GameMessage

# TODO: Let's pretend there is persistent storage   # pylint: disable=W0511
storage = {}


class Player(Requester):
    def __init__(self, base_url: str):     # pylint: disable=W0246
        super().__init__(base_url)


    async def token(self, body: TokenBody) -> None:
        url = "/api/v1/auth/token"
        method = "POST"
        response: ResponseData = await self.request(url=url, method=method, body=body.model_dump())
        jwt_response = response.json.get("jwt", "")
        storage.update({body.game_name: jwt_response})


    async def game(self, body: GameMessage) -> None:
        url = "/api/v1/game"
        method = "POST"
        token = storage.get(body.game_id, "")
        headers = {'authorization': f'Bearer {token}'}
        _response: ResponseData = await self.request(url=url, method=method, body=body, headers=headers)
