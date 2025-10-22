import pytest
from app.services.game_service import determine_winner


@pytest.mark.parametrize("p1,p2,expected", [
    ("rock", "rock", "Draw"),
    ("rock", "scissors", "Player 1"),
    ("rock", "paper", "Player 2"),
    ("paper", "rock", "Player 1"),
    ("paper", "scissors", "Player 2"),
    ("scissors", "paper", "Player 1"),
    ("scissors", "rock", "Player 2"),
])
def test_determine_winner(p1, p2, expected):
    assert determine_winner(p1, p2) == expected
