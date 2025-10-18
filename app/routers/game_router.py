from fastapi import APIRouter, Request, HTTPException
from app.schemas.game_schema import CreateGameResponse, PlayMoveRequest, GameResult
from app.services import game_service
from uuid import UUID

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/create", response_model=CreateGameResponse)
def create_game(request: Request):
    base_url = str(request.base_url).rstrip('/')
    return game_service.create_game(base_url)


@router.post("/join/{game_id}")
def join_game(game_id: UUID):
    result = game_service.join_game(game_id)
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{game_id}/play", response_model=GameResult)
def play_move(game_id: UUID, payload: PlayMoveRequest):
    result = game_service.play_move(game_id, payload.player_id, payload.move.value)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid player or game")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
