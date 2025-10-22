from uuid import uuid4, UUID
from typing import Optional
from app.schemas.game_schema import Move, GameState


class Game:
    def __init__(self):
        self.id = uuid4()
        self.player1_id = uuid4()
        self.player2_id: Optional[UUID] = None
        self.player1_move: Optional[Move] = None
        self.player2_move: Optional[Move] = None
        self.state: GameState = GameState.created
        self.winner = None

    def __str__(self) -> str:
        return (
            f"Game(id={self.id}, player1_id={self.player1_id}, "
            f"player2_id={self.player2_id}, player1_move={self.player1_move}, "
            f"player2_move={self.player2_move}, state={self.state}, winner={self.winner})"
        )


games_db: dict[UUID, Game] = {}
