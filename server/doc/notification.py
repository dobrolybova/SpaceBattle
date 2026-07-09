from enum import Enum

from openapi_pydantic import OpenAPI
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

from pydantic import BaseModel

class Event(str, Enum):
    TOURNAMENT_STARTED = "TOURNAMENT_STARTED"
    TOURNAMENT_ANNOUNCED = "TOURNAMENT_ANNOUNCED"
    BATTLE_IS_STARTED = "BATTLE_IS_STARTED"
    BATTLE_IS_STARTED_SOON = "BATTLE_IS_STARTED_SOON"
    BATTLE_IS_FINISHED = "BATTLE_IS_FINISHED"


class Subscribe(BaseModel):
    user_id: int
    events: list[Event]


def construct_base_open_api() -> OpenAPI:
    return OpenAPI.model_validate({
        "info": {"title": "Space battle API: Notification part.", "version": "1.0.0"},
        "servers": [{"url": "/api/v1/notification"}],
        "paths": {
            "/subscribe": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "User subscribes on list of events.",
                         },
                        "403": {
                            "description": "User not authorised.",
                        },
                        "400": {
                            "description": "Event not exists.",
                        }
                    },
                    "requestBody": {
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=Subscribe)
                        }}
                    }
                }
            },
            "/ws": {
            }
        }
    })


open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

if __name__ == '__main__':
    with open("notifications.json", "w") as file:
        file.write(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=4))
