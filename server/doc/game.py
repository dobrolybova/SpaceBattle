from enum import Enum

from openapi_pydantic import OpenAPI
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

from pydantic import BaseModel

class GametStatus(str, Enum):
    STARTED = "STARTED"
    NOT_STARTED = "NOT_STARTED"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class Tournament(BaseModel):
    id: int
    name: str


class Game(BaseModel):
    id: int
    name: str
    data: dict
    tournaments: list[Tournament]


class Games(BaseModel):
    games: list[Game]


class GameReq(BaseModel):
    user_id: int
    game_name: str
    tournament: Tournament


class GameResp(BaseModel):
    game_id: int
    game_name: str
    game_status: GametStatus
    message: str
    tournaments: list[Tournament]


def construct_base_open_api() -> OpenAPI:
    return OpenAPI.model_validate({
        "info": {"title": "Space battle API: Game part.", "version": "1.0.0"},
        "servers": [{"url": "/api/v1/games"}],
        "paths": {
            "/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "List of all games.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Games)
                                }
                            }
                        }
                    },
                },
            },
            "/{game_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Data for particular game.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Game)
                                }
                            }
                        }
                    },
                },
            },
            "/join": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "User joins to the game.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=GameResp)
                                }
                            }
                        },
                        "400": {
                            "description": "Wrong game or game is already started.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=GameResp)
                                }
                            }
                        },
                        "403": {
                            "description": "User is not authorised.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=GameResp)
                                }
                            }
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=GameReq)
                        }}
                    }
                },
            },
            "/new": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "User creates new game.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=GameResp)
                                }
                            }
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=GameReq)
                        }}
                    }
                },
            },
        }
    })


open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

if __name__ == '__main__':
    with open("game.json", "w") as file:
        file.write(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=4))
