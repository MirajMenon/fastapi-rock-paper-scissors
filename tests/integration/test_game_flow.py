def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"status": "OK"}


def test_create_and_join(client, created_game):
    gid = created_game["game_id"]
    j = client.post(f"/game/join/{gid}")
    assert j.status_code == 200
    assert j.json()["game_id"] == gid
    assert "player2_id" in j.json()


def test_first_player_waits_then_resolves(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]
    p2 = joined_game["player2_id"]

    r1 = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "rock"})
    assert r1.status_code == 200
    assert r1.json()["winner"] is None
    assert r1.json()["message"] == "Waiting for the other player to play"

    r2 = client.post(f"/game/{gid}/play", json={"player_id": p2, "move": "scissors"})
    assert r2.status_code == 200
    body = r2.json()
    assert body["winner"] == "Player 1"
    assert body["player1_move"] == "rock"
    assert body["player2_move"] == "scissors"

    # First player can “poll” by using get results
    r3 = client.get(f"/game/{gid}/results")
    assert r3.status_code == 200
    assert r3.json()["winner"] == "Player 1"


def test_draw_result(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]
    p2 = joined_game["player2_id"]
    client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "paper"})
    res = client.post(f"/game/{gid}/play", json={"player_id": p2, "move": "paper"})
    assert res.status_code == 200
    assert res.json()["winner"] == "Draw"
