from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Optional


class Move(str, Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


class CreateGameResponse(BaseModel):
    game_id: UUID
    player1_id: UUID
    join_url: str


class PlayMoveRequest(BaseModel):
    player_id: UUID
    move: Move


class GameResult(BaseModel):
    winner: Optional[str]
    player1_move: Optional[Move] = None
    player2_move: Optional[Move] = None
    message: Optional[str] = None

