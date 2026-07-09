from enum import Enum

from openapi_pydantic import OpenAPI
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

from pydantic import BaseModel

class UserStatus(str, Enum):
    NOT_REGISTERED = "NOT_REGISTERED"
    REGISTERED = "REGISTERED"
    LOGGED_IN = "LOGGED_IN"


class UserResp(BaseModel):
    user_id: int
    user_status: UserStatus
    message: str


class UserReq(BaseModel):
    name: str


def construct_base_open_api() -> OpenAPI:
    return OpenAPI.model_validate({
        "info": {"title": "Space battle API: Authorisation part.", "version": "1.0.0"},
        "servers": [{"url": "/api/v1/auth"}],
        "paths": {
            "/register": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Register user. "
                                           "Receive user name and password in header, response with new unique user id and REGISTERED user status. "
                                           "Message contains some additional info if needed.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=UserResp)
                                }
                            }
                        }
                    },
                }
            },
            "/login": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Login user OK. "
                                           "Receive user name and password in header, response with user id and LOGGED_IN user status. "
                                           "Message contains some additional info if needed.",
                            "content": {
                                "application/json": {
                                "schema": PydanticSchema(schema_class=UserResp)
                                }
                            }
                        },
                        "403": {
                            "description": "Login user forbidden. "
                                           "Receive user name and password in header, response with user id and NOT_REGISTERED/REGISTERED user status. "
                                           "Additional info (if user registered or not and if password is correct) is in message field.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=UserResp)
                                }
                            }
                        }
                    }
                }
            },
            "/logout": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Logged out user OK. "
                                           "Response with user id and REGISTERED user status. "
                                           "Message contains some additional info if needed.",
                            "content": {
                                "application/json": {
                                "schema": PydanticSchema(schema_class=UserResp)
                                }
                            }
                        },
                         "400": {
                            "description": "Logged out user bad request. "
                                           "Response with user id and NOT_REGISTERED/REGISTERED user status. "
                                           "Additional info (if user registered and logged in or not) is in message field.",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=UserResp)
                                }
                            }
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=UserReq)
                        }}
                    }
                }
            },
            "/status": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Get user status: NOT_REGISTERED/REGISTERED/LOGGED_IN",
                            "content": {
                                "application/json": {
                                    "schema": PydanticSchema(schema_class=UserResp)
                                }
                            },
                        },
                    },
                }
            }
        }
    })


open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

if __name__ == '__main__':
    with open("auth.json", "w") as file:
        file.write(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=4))
