import pytest
from unittest.mock import Mock
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre
from games.browse import services
from flask import Flask
from games.adapters.memory_repository import MemoryRepository, populate2 as populate



@pytest.fixture
def memory_repo():
    memory_repo = MemoryRepository()
    #populate(memory_repo)
    game1 = Game(1, "Game 1")
    game1.add_genre(Genre("Action"))
    game1.add_genre(Genre("Adventure"))

    game2 = Game(2, "Game 2")
    game2.add_genre(Genre("RPG"))
    game2.add_genre(Genre("Adventure"))

    game3 = Game(3, "Game 3")
    game3.add_genre(Genre("Puzzle"))
    game3.add_genre(Genre("Strategy"))
    memory_repo.add_game(game1)
    memory_repo.add_game(game3)
    memory_repo.add_game(game2)
    return memory_repo


def test_get_games_by_genre(memory_repo):
    genre = "Adventure"
    result = services.get_games_by_genre(memory_repo, genre)
    assert len(result) == 2



def test_get_games_by_invalid_genre(memory_repo):
    genre = "Unknown Genre"
    result = memory_repo.get_games_by_genre(genre)
    assert len(result) == 0


def test_get_games_by_all_genre(memory_repo):
    genre = "All"
    result = memory_repo.get_games_by_genre(genre)
    assert len(result) == 3


def test_get_game_genres(memory_repo):
    result = services.get_game_genres(memory_repo)
    assert result == ["Action", "Adventure", "Puzzle", "RPG", "Strategy"]



def test_get_games_pagination(memory_repo):
    app = Flask(__name__)
    with app.app_context():
        with app.test_request_context('/'):
            result = memory_repo.get_games_pagination( offset=0, limit=1)
            assert len(result) == 1
            assert result[0]["game_id"] == 1

            result = memory_repo.get_games_pagination(offset=1, limit=1)
            assert len(result) == 1
            assert result[0]["game_id"] == 2



def test_get_games_pagination_with_genre(memory_repo):
    app = Flask(__name__)
    with app.app_context():
        with app.test_request_context('/'):
            result = memory_repo.get_games_pagination(genre="Adventure", offset=0, limit=1)
            assert len(result) == 1
            assert result[0]["game_id"] == 1

