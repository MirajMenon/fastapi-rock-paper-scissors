import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.game_model import games_db


@pytest.fixture(autouse=True)
def _clear_db():
    games_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_game(client):
    res = client.post("/game/create")
    assert res.status_code == 200
    return res.json()


@pytest.fixture
def joined_game(client, created_game):
    gid = created_game["game_id"]
    res = client.post(f"/game/join/{gid}")
    assert res.status_code == 200
    return {**created_game, **res.json()}
