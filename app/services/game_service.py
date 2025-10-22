from uuid import uuid4
from sqlalchemy.orm import Session
from app.database.database_model import Game, GameState, Move
from app.schemas.game_schema import GameState as SchemaGameState, Move as SchemaMove


def create_game(db: Session, base_url: str):
    game = Game()
    db.add(game)
    db.commit()
    db.refresh(game)
    return {
        "game_id": game.id,
        "player1_id": game.player1_id,
        "game_state": SchemaGameState(game.state.value),
        "join_url": f"{base_url}/game/join/{game.id}",
    }


def join_game(db: Session, game_id):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None
    if game.player2_id:
        return {"error": "Game already has two players"}
    game.player2_id = uuid4()
    game.state = GameState.joined
    db.commit()
    db.refresh(game)
    return {"game_id": game.id, "player2_id": game.player2_id, "game_state": SchemaGameState(game.state.value)}


def determine_winner(p1_move, p2_move):
    # Convert enum values to strings for comparison
    p1_str = p1_move.value if hasattr(p1_move, 'value') else str(p1_move)
    p2_str = p2_move.value if hasattr(p2_move, 'value') else str(p2_move)
    
    if p1_str == p2_str:
        return "Draw"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if wins[p1_str] == p2_str:
        return "Player 1"
    return "Player 2"


def play_move(db: Session, game_id, player_id, move: SchemaMove):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None

    if game.state == GameState.finished:
        return {"error": "Game already finished"}

    # Convert schema move to database move
    db_move = Move(move.value)

    # Assign the move to the correct player
    if player_id == game.player1_id:
        if game.player1_move is not None:
            return {"error": "You have already moved"}
        game.player1_move = db_move
    elif player_id == game.player2_id:
        if game.player2_move is not None:
            return {"error": "You have already moved"}
        game.player2_move = db_move
    else:
        return {"error": "Invalid player"}

    # Check if both players have played
    if game.player1_move and game.player2_move:
        game.winner = determine_winner(game.player1_move, game.player2_move)
        game.state = GameState.finished
        db.commit()
        db.refresh(game)
        return {
            "winner": game.winner,
            "player1_move": SchemaMove(game.player1_move.value),
            "player2_move": SchemaMove(game.player2_move.value),
            "game_state": SchemaGameState(game.state.value),
            "message": (
                "It's a Draw!" if game.winner == "Draw" else f"{game.winner} Wins!"
            ),
        }

    db.commit()
    db.refresh(game)
    return {
        "message": "Waiting for the other player to play",
        "player1_move": SchemaMove(game.player1_move.value) if game.player1_move else None,
        "player2_move": SchemaMove(game.player2_move.value) if game.player2_move else None,
        "game_state": SchemaGameState(game.state.value),
        "winner": None,
    }


def get_results(db: Session, game_id):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None

    if game.player1_move and game.player2_move:
        return {
            "winner": game.winner,
            "player1_move": SchemaMove(game.player1_move.value),
            "player2_move": SchemaMove(game.player2_move.value),
            "game_state": SchemaGameState(game.state.value),
            "message": (
                "It's a Draw!" if game.winner == "Draw" else f"{game.winner} Wins!"
            ),
        }

    return {
        "message": "Waiting for the other player to play",
        "player1_move": SchemaMove(game.player1_move.value) if game.player1_move else None,
        "player2_move": SchemaMove(game.player2_move.value) if game.player2_move else None,
        "game_state": SchemaGameState(game.state.value),
        "winner": None,
    }
