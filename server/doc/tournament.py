from enum import Enum
from typing import Optional

from openapi_pydantic import OpenAPI
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

from pydantic import BaseModel


class TournamentStatus(str, Enum):
    STARTED = "STARTED"
    NOT_STARTED = "NOT_STARTED"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class Result(BaseModel):
    data: dict


class Participant(BaseModel):
    id: int
    name: str


class Tournament(BaseModel):
    id: int
    name: str
    status: TournamentStatus
    participants: list[Participant]
    result: Result


class TournamentReq(BaseModel):
    status: Optional[TournamentStatus]
    participant: Optional[Participant]


class Tournaments(BaseModel):
    tournaments: list[Tournament]


class Rating(BaseModel):
    participant: Optional[Participant]
    value: int
    tournament_name: Optional[str]


class Ratings(BaseModel):
    Ratings: list[Rating]


def construct_base_open_api() -> OpenAPI:
    return OpenAPI.model_validate({
        "info": {"title": "Space battle API: Tournament part.", "version": "1.0.0"},
        "servers": [{"url": "/api/v1/tournaments"}],
        "paths": {
            "/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "List of all tournament with its data.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Tournaments)
                                }
                            }
                        }
                    },
                },
            },
            "/{tournament}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Data for particular tournament.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Tournament)
                                }
                            }
                        }
                    },
                },
            },
            "/{tournament}": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Update tournament data.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Tournament)
                                }
                            }
                        },
                        "400": {
                            "description": "Wrong tournament status.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Tournament)
                                }
                            }
                        },
                        "403": {
                            "description": "Participant is not authorised.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Tournament)
                                }
                            }
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=TournamentReq)
                        }}
                    }
                },
            },
            "/{tournament}/ratings": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Ratings data for particular tournament.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Ratings)
                                }
                            }
                        }
                    },
                },
            },
            "/ratings/{participant}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Ratings data for particular user.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=Ratings)
                                }
                            }
                        }
                    },
                },
            },
            "/ratings/calculate": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Update ratings data.",
                        },
                        "400": {
                            "description": "Wrong received data.",
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=Rating)
                        }}
                    }
                },
            },
        }
    })


open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

if __name__ == '__main__':
    with open("tournament.json", "w") as file:
        file.write(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=4))
