from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.game_schema import (
    CreateGameResponse,
    PlayMoveRequest,
    GameResult,
    JoinGameResponse,
)
from app.services import game_service
from app.database.database import get_db
from uuid import UUID

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/create", response_model=CreateGameResponse)
def create_game(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    return game_service.create_game(db, base_url)


@router.post("/join/{game_id}", response_model=JoinGameResponse)
def join_game(game_id: UUID, db: Session = Depends(get_db)):
    result = game_service.join_game(db, game_id)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{game_id}/play", response_model=GameResult)
def play_move(game_id: UUID, payload: PlayMoveRequest, db: Session = Depends(get_db)):
    result = game_service.play_move(db, game_id, payload.player_id, payload.move)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid player or game")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{game_id}/results", response_model=GameResult)
def get_results(game_id: UUID, db: Session = Depends(get_db)):
    result = game_service.get_results(db, game_id)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid game")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
