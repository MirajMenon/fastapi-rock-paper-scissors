import uuid


def test_join_missing_game_returns_404(client):
    gid = uuid.uuid4()
    res = client.post(f"/game/join/{gid}")
    assert res.status_code == 404


def test_join_full_returns_400(client, joined_game):
    gid = joined_game["game_id"]
    res = client.post(f"/game/join/{gid}")
    assert res.status_code == 400
    assert "Game already has two players" in res.json()["detail"]


def test_play_with_invalid_player_returns_400(client, created_game):
    gid = created_game["game_id"]
    bogus_player = str(uuid.uuid4())
    res = client.post(
        f"/game/{gid}/play", json={"player_id": bogus_player, "move": "rock"}
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid player"
