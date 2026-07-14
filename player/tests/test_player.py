from unittest.mock import patch
import pytest
from aiohttp import ContentTypeError, ClientConnectorError

from player.src.player import Player, storage
from player.src.schemas import TokenBody

from server.src.enums import OperationId
from server.src.schemas import GameMessage, MoveArgs


class MockResponse:
    def __init__(self, js, status):
        self.js = js
        self.status = status

    async def json(self):
        return self.js

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    def raise_for_status(self):
        return


class MockResponseText:
    def __init__(self, txt, status):
        self.txt = txt
        self.status = status

    async def json(self):
        raise ContentTypeError(request_info=None, history=None)

    async def text(self):
        return self.txt

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    def raise_for_status(self):
        return


@pytest.mark.asyncio
async def test_jwt():
    resp = MockResponse(js={"jwt": "jwt.jwt.jwt"}, status=200)
    assert not storage
    with patch("player.src.requester.Requester.get_session", return_value=resp):
        player = Player(base_url="http://localhost:8080")
        await player.token(body=TokenBody(game_name="game_1234"))
    assert storage == {'game_1234': 'jwt.jwt.jwt'}


@pytest.mark.asyncio
async def test_game():
    resp = MockResponse(js={"jwt": "jwt.jwt.jwt"}, status=200)
    with patch("player.src.requester.Requester.get_session", return_value=resp):
        player = Player(base_url="http://localhost:8080")
        await player.game(GameMessage(
            game_id="game_123", object_id="ship1", operation_id=OperationId.ROTATION, args=MoveArgs()))

@pytest.mark.asyncio
async def test_text():
    resp = MockResponseText(txt="Some text", status=200)
    with patch("player.src.requester.Requester.get_session", return_value=resp):
        player = Player(base_url="http://localhost:8080")
        await player.token(body=TokenBody(game_name="game_1234"))


@pytest.mark.asyncio
async def test_no_connection():
    with pytest.raises(ClientConnectorError):
        player = Player(base_url="http://localhost:8080")
        await player.token(body=TokenBody(game_name="game_1234"))
