from uuid import uuid4
from app.models.game_model import games_db, Game
from app.schemas.game_schema import GameState, Move


def create_game(base_url: str):
    game = Game()
    games_db[game.id] = game
    return {
        "game_id": game.id,
        "player1_id": game.player1_id,
        "game_state": game.state,
        "join_url": f"{base_url}/game/join/{game.id}",
    }


def join_game(game_id):
    game = games_db.get(game_id)
    if not game:
        return None
    if game.player2_id:
        return {"error": "Game already has two players"}
    game.player2_id = uuid4()
    game.state = GameState.joined
    return {"game_id": game.id, "player2_id": game.player2_id, "game_state": game.state}


def determine_winner(p1_move, p2_move):
    if p1_move == p2_move:
        return "Draw"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if wins[p1_move] == p2_move:
        return "Player 1"
    return "Player 2"


def play_move(game_id, player_id, move: Move):
    game = games_db.get(game_id)
    if not game:
        return None

    if game.state == GameState.finished:
        return {"error": "Game already finished"}

    # Assign the move to the correct player
    if player_id == game.player1_id:
        if game.player1_move is not None:
            return {"error": "You have already moved"}
        game.player1_move = move
    elif player_id == game.player2_id:
        if game.player2_move is not None:
            return {"error": "You have already moved"}
        game.player2_move = move
    else:
        return {"error": "Invalid player"}

    # Check if both players have played
    if game.player1_move and game.player2_move:
        game.winner = determine_winner(game.player1_move, game.player2_move)
        game.state = GameState.finished
        return {
            "winner": game.winner,
            "player1_move": game.player1_move,
            "player2_move": game.player2_move,
            "game_state": game.state,
            "message": (
                "It's a Draw!" if game.winner == "Draw" else f"{game.winner} Wins!"
            ),
        }

    return {
        "message": "Waiting for the other player to play",
        "player1_move": game.player1_move,
        "player2_move": game.player2_move,
        "game_state": game.state,
        "winner": None,
    }


def get_results(game_id):
    game = games_db.get(game_id)
    if not game:
        return None

    if game.player1_move and game.player2_move:
        return {
            "winner": game.winner,
            "player1_move": game.player1_move,
            "player2_move": game.player2_move,
            "game_state": game.state,
            "message": (
                "It's a Draw!" if game.winner == "Draw" else f"{game.winner} Wins!"
            ),
        }

    return {
        "message": "Waiting for the other player to play",
        "player1_move": game.player1_move,
        "player2_move": game.player2_move,
        "game_state": game.state,
        "winner": None,
    }
