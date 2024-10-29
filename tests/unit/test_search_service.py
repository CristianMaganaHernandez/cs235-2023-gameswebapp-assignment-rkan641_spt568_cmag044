import pytest
from unittest.mock import Mock

from games import MemoryRepository
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher
import games.adapters.repository as repo


# @pytest.fixture
# def mock_repo():
#     repo = Mock(spec=AbstractRepository)
#     mock_game = Game(1, "Game Title")
#     mock_game.price = 59.99
#     action_genre = Genre("Action")
#     mock_game.add_genre(action_genre)
#     mock_game.publisher = Publisher("Publisher Name")
#     repo.get_games.return_value = [mock_game]
#     return repo
import pytest
from games.adapters.memory_repository import MemoryRepository, populate2
from games.domainmodel.model import Game, Genre, Publisher
from games.search import services

@pytest.fixture
def memory_repo():
    memory_repo = MemoryRepository()
    #populate(memory_repo)

    game1 = Game(1, "Game 1")
    game1.add_genre(Genre("Action"))
    game1.add_genre(Genre("Adventure"))
    publish = Publisher("ME")
    game1.publisher = publish
    game1.price = 535

    game2 = Game(2, "Game 2")
    game2.add_genre(Genre("RPG"))
    game2.add_genre(Genre("Adventure"))
    game2.publisher = publish
    game2.price = 5

    game3 = Game(3, "Game 3")
    game3.add_genre(Genre("Puzzle"))
    game3.add_genre(Genre("Strategy"))
    game3.publisher = publish
    game3.price = 45

    memory_repo.add_game(game1)
    memory_repo.add_game(game3)
    memory_repo.add_game(game2)
    return memory_repo


def test_service_returns_existing_game(memory_repo):
    results = services.search_games(memory_repo,'Game Title', 'Title', [])
    assert results == [game for game in memory_repo.get_games() if 'Game Title' in game.title]

def test_service_retrieves_correct_number_of_games(memory_repo):
    assert len(memory_repo.search_games('Game 1', 'Title', [])) == 1

def test_getting_games_for_search_key_genre(memory_repo):
    results = memory_repo.search_games('Action', 'Genre', [])
    assert results == [game for game in memory_repo.get_games() if 'Action' in [genre.genre_name for genre in game.genres]]

def test_getting_games_for_search_key_publisher(memory_repo):
    results = services.search_games(memory_repo,'ME', 'Publisher', [])
    assert len(results) == 3

def test_inserting_non_existing_search_key_throws_exception(memory_repo):
    assert memory_repo.search_games('food', 'All', []) == []

def test_getting_games_for_price(memory_repo):
    results = memory_repo.search_games('a', 'Title', ["40-70"])
    assert len(results) == 1

if __name__ == "__main__":
    pytest.main()


