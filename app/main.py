from fastapi import FastAPI
from app.routers import game_router

app = FastAPI(title="Rock Paper Scissors API")

app.include_router(game_router.router)


@app.get("/")
def health_check():
    return {"status": "OK"}
