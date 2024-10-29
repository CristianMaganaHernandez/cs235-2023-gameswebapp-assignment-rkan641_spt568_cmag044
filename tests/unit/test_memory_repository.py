import pytest
from games.adapters.memory_repository import MemoryRepository, populate2 as populate
from games.domainmodel.model import Game, Publisher, User


def test_populate_function():
    repo = MemoryRepository()
    populate(repo)
    assert repo.get_number_of_games() == 877


@pytest.fixture
def memory_repo():
    repo = MemoryRepository()
    populate(repo)
    return repo


def test_get_number_of_games(memory_repo):
    assert memory_repo.get_number_of_games() == 877


def test_add_game(memory_repo):

    # Input correct class
    game = Game(999, "Test Game")
    memory_repo.add_game(game)
    assert memory_repo.get_number_of_games() == 878

    # Input incorrect class
    game2 = Publisher("Bethesda")
    memory_repo.add_game(game2)
    assert memory_repo.get_number_of_games() == 878


def test_get_games(memory_repo):
    games = memory_repo.get_games()

    # Check if memory_repo.get_games() returns correct number of games
    assert len(games) == memory_repo.get_number_of_games()

    # Check memory_repo.get_games() returns list
    assert isinstance(games, list)

    # Check if memory_repo contains a list of only Games classes
    assert all(isinstance(game, Game) for game in games)


# Check if all game_id's are sorted
def test_repository_sorted_by_id(memory_repo):
    games = memory_repo.get_games()

    # Check if games are sorted by id
    assert all(game1.game_id <= game2.game_id for game1, game2 in zip(games, games[1:]))

    # Check if games are sorted when added
    new_game1 = Game(0, "Test Game 1")
    new_game2 = Game(99999999, "Test Game 2")

    # Realistic id -- one more than an id that is in the data set
    new_game3 = Game(435791, "Test Game 3")

    memory_repo.add_game(new_game1)
    memory_repo.add_game(new_game2)
    memory_repo.add_game(new_game3)

    assert games[0] == new_game1
    assert games[-1] == new_game2
    assert all(game1.game_id <= game2.game_id for game1, game2 in zip(games, games[1:]))


def test_add_get_user(memory_repo):

    new_user = User("Bob", "test123")
    memory_repo.add_user(new_user)

    # Correct username
    assert memory_repo.get_user(new_user.username) == new_user

    # Incorrect username
    assert memory_repo.get_user("afasfas") is None


def test_service_returns_existing_game(memory_repo):
    results = memory_repo.search_games('Game Title', 'Title', [])
    assert results == [game for game in memory_repo.get_games() if 'Game Title' in game.title]

def test_service_retrieves_correct_number_of_games(memory_repo):
    assert len(memory_repo.search_games('Game Title', 'Title', [])) == 0

def test_getting_games_for_search_key_genre(memory_repo):
    results = memory_repo.search_games('Action', 'Genre', [])
    assert results == [game for game in memory_repo.get_games() if 'Action' in [genre.genre_name for genre in game.genres]]

def test_getting_games_for_search_key_publisher(memory_repo):
    results = memory_repo.search_games('Acti', 'Publisher', [])
    assert results != []

def test_inserting_non_existing_search_key_throws_exception(memory_repo):
    assert memory_repo.search_games('food', 'All', []) == []

def test_getting_games_for_price(memory_repo):
    results = memory_repo.search_games('a', 'Title', ["40-70"])
    assert results != []
