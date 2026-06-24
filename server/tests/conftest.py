import pytest
from fastapi.testclient import TestClient

from server.src.endpoint import app


class TestException(Exception):
    def __init__(self, msg=""):
        super().__init__()
        self.msg = msg

    def get_msg(self) -> str:
        return self.msg

    def __repr__(self):
        return self.msg


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
