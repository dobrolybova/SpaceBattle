import uuid
from http import HTTPStatus
from unittest.mock import patch

import jwt


def test_not_found(client):
    res = client.post("/unknown")
    assert res.json() == {'detail': 'Not Found'}
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_method_not_allowed_token(client):
    res = client.put("/api/v1/auth/token")
    assert res.json() == {'detail': 'Method Not Allowed'}
    assert res.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_method_not_allowed_new_game(client):
    res = client.put("/api/v1/auth/new_game")
    assert res.json() == {'detail': 'Method Not Allowed'}
    assert res.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_unprocessable_token(client):
    res = client.post(url="/api/v1/auth/token", json={})
    assert res.json() == {'detail': [{'input': {},
                                      'loc': ['body', 'game_name'],
                                      'msg': 'Field required',
                                      'type': 'missing'}]}
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_unprocessable_new_game(client):
    res = client.post(url="/api/v1/auth/new_game", json={})
    assert res.json() == {'detail': [{'input': {},
                                      'loc': ['body', 'participants'],
                                      'msg': 'Field required',
                                      'type': 'missing'}]}
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@patch.object(uuid, "uuid4", return_value="1234")
def test_new_game(_mock, client):
    res = client.post(url="/api/v1/auth/new_game", json={"participants": ["user1", "user2"]})
    assert res.json() == {'game_name': 'game_1234', 'user_name': ''}
    assert res.status_code == HTTPStatus.OK


@patch.object(uuid, "uuid4", return_value="1234")
def test_new_token_no_game(_mock, client):
    res = client.post(url="/api/v1/auth/token", json={'game_name': 'game_4321', 'user_name': 'user2'})
    assert res.json() == {'detail': 'Game game_4321 not exists'}
    assert res.status_code == HTTPStatus.BAD_REQUEST


@patch.object(uuid, "uuid4", return_value="1234")
def test_new_token_no_player(_mock, client):
    client.post(url="/api/v1/auth/new_game", json={"participants": ["user1", "user2"]})
    res = client.post(url="/api/v1/auth/token", json={'game_name': 'game_1234', 'user_name': 'user3'})
    assert res.json() == {'detail': 'Player user3 not in game game_1234'}
    assert res.status_code == HTTPStatus.BAD_REQUEST


@patch.object(uuid, "uuid4", return_value="1234")
def test_new_token(_mock, client):
    client.post(url="/api/v1/auth/new_game", json={"participants": ["user1", "user2"]})
    res = client.post(url="/api/v1/auth/token", json={'game_name': 'game_1234', 'user_name': 'user2'})
    resp = res.json()
    assert resp == {"jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnYW1lX25hbWUiOiJnYW1lXzEyMzQiLCJ1c2VyX25hbWUiOiJ1c2VyMiJ9.ApHiO_m3nx3I-TwVQBs8V56d93mhXR-CWBs8SYY73tA"}  # pylint: disable=C0301
    jwt_content = jwt.decode(resp.get("jwt"), "secret", algorithms=["HS256"])
    assert jwt_content == {'game_name': 'game_1234', 'user_name': 'user2'}
    assert res.status_code == HTTPStatus.OK
