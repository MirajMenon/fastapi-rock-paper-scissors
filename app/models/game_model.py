from uuid import uuid4
from typing import Optional
from app.schemas.game_schema import Move


class Game:
    def __init__(self):
        self.id = uuid4()
        self.player1_id = uuid4()
        self.player2_id: Optional[uuid4] = None
        self.player1_move: Optional[Move] = None
        self.player2_move: Optional[Move] = None

    def __str__(self):
        return f"Game(id={self.id}, player1_id={self.player1_id}, player2_id={self.player2_id}, player1_move={self.player1_move}, player2_move={self.player2_move})"


games_db = {}
