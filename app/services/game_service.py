from uuid import uuid4

from app.models.game_model import games_db, Game


def create_game(base_url: str):
    game = Game()
    games_db[game.id] = game
    return {
        "game_id": game.id,
        "player1_id": game.player1_id,
        "join_url": f"{base_url}/game/join/{game.id}"
    }


def join_game(game_id):
    game = games_db.get(game_id)
    if not game:
        return None
    if game.player2_id:
        return {"error": "Game already has two players"}
    game.player2_id = uuid4()
    return {"game_id": game.id, "player2_id": game.player2_id}


def determine_winner(p1_move, p2_move):
    if p1_move == p2_move:
        return "Draw"
    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }
    if wins[p1_move] == p2_move:
        return "Player 1"
    return "Player 2"


def play_move(game_id, player_id, move):
    game = games_db.get(game_id)
    if not game:
        return None

    # Assign the move to the correct player
    if player_id == game.player1_id:
        game.player1_move = move
    elif player_id == game.player2_id:
        game.player2_move = move
    else:
        return {"error": "Invalid player"}

    # Check if both players have played
    if game.player1_move and game.player2_move:
        winner = determine_winner(game.player1_move, game.player2_move)
        return {
            "winner": winner,
            "player1_move": game.player1_move,
            "player2_move": game.player2_move
        }

    return {
        "message": "Waiting for the other player to play",
        "player1_move": game.player1_move,
        "player2_move": game.player2_move,
        "winner": None
    }