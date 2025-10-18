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

### API Endpoints

1. Create a game

   POST `/game/create`

   Response:

   ```json
   {
     "game_id": "UUID",
     "player1_id": "UUID",
     "join_url": "http://127.0.0.1:8000/game/join/<game_id>"
   }
   ```

2. Join a game

   POST `/game/join/{game_id}`

   Response:

   ```json
   {
     "game_id": "UUID",
     "player2_id": "UUID"
   }
   ```

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
     "message": "Waiting for the other player to play"
   }
   ```

   Response (round resolved):

   ```json
   {
     "winner": "Player 2",
     "player1_move": "rock",
     "player2_move": "paper",
     "message": null
   }
   ```

4. Health check

   GET `/`

   Response:

   ```json
   { "status": "OK" }
   ```

## Suggested Next Steps and Enhancements

If I had more time, here are some ways I would improve the project:

- **Persistent storage**: Currently, the game uses an in-memory database (`games_db`), so restarting the server clears all games. I would use a database to make game data persistent.

- **Test cases**: I would write tests to cover all possible move combinations and edge cases.

- **Better error handling**: I would implement more descriptive errors and proper HTTP status codes for invalid moves or other edge cases.

- **Authentication**: I would add player authentication to ensure moves are secure and players cannot impersonate others.
