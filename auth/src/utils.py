import uuid

# TODO: let's pretend there is DB'    # pylint: disable=W0511
participants = {}


def update_participants(new_participants: list[str]) -> str:
    new_game = f"game_{str(uuid.uuid4())}"
    participants.update({new_game: new_participants})
    return new_game
