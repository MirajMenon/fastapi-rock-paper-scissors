from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database.database import Base
import enum
import uuid


class GameState(str, enum.Enum):
    created = "Created"
    joined = "Joined"
    finished = "Finished"


class Move(str, enum.Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"


class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player1_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    player2_id = Column(UUID(as_uuid=True), nullable=True)
    player1_move = Column(Enum(Move), nullable=True)
    player2_move = Column(Enum(Move), nullable=True)
    state = Column(Enum(GameState), nullable=False, default=GameState.created)
    winner = Column(String, nullable=True)
