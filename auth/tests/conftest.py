import pytest
from starlette.testclient import TestClient

from auth.src.endpoint import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
