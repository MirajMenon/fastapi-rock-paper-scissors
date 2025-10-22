import uuid


def test_same_player_move_twice_returns_400(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]

    r1 = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "rock"})
    assert r1.status_code == 200

    r2 = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "paper"})
    assert r2.status_code == 400
    assert r2.json()["detail"] == "You have already moved"


def test_play_after_game_finished_returns_400(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]
    p2 = joined_game["player2_id"]

    # Finish the game
    r1 = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "rock"})
    assert r1.status_code == 200
    r2 = client.post(
        f"/game/{gid}/play", json={"player_id": p2, "move": "scissors"}
    )
    assert r2.status_code == 200
    assert r2.json()["winner"] in {"Player 1", "Player 2", "Draw"}

    # Any subsequent play must error
    r3 = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "rock"})
    assert r3.status_code == 400
    assert r3.json()["detail"] == "Game already finished"


def test_results_waiting_before_both_moves(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]

    client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "paper"})

    res = client.get(f"/game/{gid}/results")
    assert res.status_code == 200
    body = res.json()
    assert body["message"] == "Waiting for the other player to play"
    assert body["winner"] is None
    assert body["game_state"] == "Joined"


def test_results_invalid_game_returns_404(client):
    gid = uuid.uuid4()
    res = client.get(f"/game/{gid}/results")
    assert res.status_code == 404
    assert res.json()["detail"] == "Invalid game"


def test_prejoin_player1_can_play_waiting_state(client, created_game):
    gid = created_game["game_id"]
    p1 = created_game["player1_id"]

    res = client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "rock"})
    assert res.status_code == 200
    body = res.json()
    assert body["message"] == "Waiting for the other player to play"
    assert body["winner"] is None
    assert body["game_state"] == "Created" or body["game_state"] == "Joined"


def test_prejoin_player2_cannot_play_returns_400(client, created_game):
    gid = created_game["game_id"]
    bogus_player = str(uuid.uuid4())

    res = client.post(
        f"/game/{gid}/play", json={"player_id": bogus_player, "move": "scissors"}
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid player"


def test_invalid_move_value_returns_422(client, joined_game):
    gid = joined_game["game_id"]
    p1 = joined_game["player1_id"]

    res = client.post(
        f"/game/{gid}/play", json={"player_id": p1, "move": "lizard"}
    )
    assert res.status_code == 422


def test_state_transitions_created_joined_finished(client, created_game):
    # Created
    assert created_game["game_state"] == "Created"
    gid = created_game["game_id"]

    # Joined
    join_res = client.post(f"/game/join/{gid}")
    assert join_res.status_code == 200
    assert join_res.json()["game_state"] == "Joined"
    p1 = created_game["player1_id"]
    p2 = join_res.json()["player2_id"]

    # Finished
    client.post(f"/game/{gid}/play", json={"player_id": p1, "move": "paper"})
    res = client.post(
        f"/game/{gid}/play", json={"player_id": p2, "move": "rock"}
    )
    assert res.status_code == 200
    assert res.json()["game_state"] == "Finished"


