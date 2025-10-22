# FastAPI Rock-Paper-Scissors

A simple Rock-Paper-Scissors game API built with FastAPI.  
Two players can create a game, join, submit moves, and see the results.

### Setup

1. Clone this repository and change into the project directory.

2. Install dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Run the application

Start the development server with uvicorn from the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Swagger docs: `http://127.0.0.1:8000/docs`.

### Run tests

From the project root, run the test suite with:

```bash
pytest
```

### API Endpoints

1. Create a game

   POST `/game/create`

   Response:

   Response body (CreateGameResponse):

   ```json
   {
     "game_id": "<uuid>",
     "player1_id": "<uuid>",
     "game_state": "Created",
     "join_url": "http://127.0.0.1:8000/game/join/<game_id>"
   }
   ```

2. Join a game

   POST `/game/join/{game_id}`

   Response body (JoinGameResponse):

   ```json
   {
     "game_id": "<uuid>",
     "player2_id": "<uuid>",
     "game_state": "Joined"
   }
   ```

   Errors:

   - 404 when the game does not exist: `{ "detail": "Game not found" }`
   - 400 when the game already has two players: `{ "detail": "Game already has two players" }`

3. Play a move

   POST `/game/{game_id}/play`

   Request body:

   ```json
   { "player_id": "<uuid>", "move": "rock|paper|scissors" }
   ```

   Response (waiting for the other player):

   ```json
   {
     "winner": null,
     "player1_move": "rock",
     "player2_move": null,
     "game_state": "Created",
     "message": "Waiting for the other player to play"
   }
   ```

   Response (round resolved):

   ```json
   {
     "winner": "Player 2",
     "player1_move": "rock",
     "player2_move": "paper",
     "game_state": "Finished",
     "message": "Player 2 Wins!"
   }
   ```

   Errors:

   - 400 when player attempts to move twice: `{ "detail": "You have already moved" }`
   - 400 when the game is finished: `{ "detail": "Game already finished" }`
   - 400 when player is invalid for the game: `{ "detail": "Invalid player" }`
   - 404 when the game does not exist: `{ "detail": "Invalid player or game" }`
   - 422 when the move is not one of `rock|paper|scissors`.

4. Get results

   GET `/game/{game_id}/results`

   Response body (GameResult):

   Waiting state:

   ```json
   {
     "winner": null,
     "player1_move": "rock",
     "player2_move": null,
     "game_state": "Joined",
     "message": "Waiting for the other player to play"
   }
   ```

   Resolved state:

   ```json
   {
     "winner": "Player 1",
     "player1_move": "paper",
     "player2_move": "rock",
     "game_state": "Finished",
     "message": "Player 1 Wins!"
   }
   ```

   Errors:

   - 404 when the game does not exist: `{ "detail": "Invalid game" }`

5. Health check

   GET `/`

   Response:

   ```json
   { "status": "OK" }
   ```

### Implementation note

This implementation uses an in-memory dictionary (`games_db`) for storing game state. If you prefer a database-backed implementation with SQLAlchemy models and sessions, refer to the database integration branch: [fastapi-rock-paper-scissors/tree/feat/database-integration](https://github.com/MirajMenon/fastapi-rock-paper-scissors/tree/feat/database-integration).
