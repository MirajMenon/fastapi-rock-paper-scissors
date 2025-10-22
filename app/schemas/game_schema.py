from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Optional


class Move(str, Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


class GameState(str, Enum):
    created = "Created"
    joined = "Joined"
    finished = "Finished"


class CreateGameResponse(BaseModel):
    game_id: UUID
    player1_id: UUID
    game_state: GameState
    join_url: str


class JoinGameResponse(BaseModel):
    game_id: UUID
    player2_id: UUID
    game_state: GameState


class PlayMoveRequest(BaseModel):
    player_id: UUID
    move: Move


class GameResult(BaseModel):
    winner: str | None = None
    player1_move: Move | None = None
    player2_move: Move | None = None
    game_state: GameState | None = None
    message: str | None = None
