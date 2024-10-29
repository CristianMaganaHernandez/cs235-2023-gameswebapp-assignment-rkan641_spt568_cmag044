import pytest
from games.domainmodel.model import User, Game
from games.adapters.memory_repository import MemoryRepository

repo = MemoryRepository()
repo.add_user(User(username="testuser", password="password123"))


@pytest.fixture
def current_user():
    return repo.get_user("testuser")


@pytest.fixture
def game():
    return Game(game_id=1, game_title="Test Game")


@pytest.fixture
def another_game():
    return Game(game_id=2, game_title="Another Test Game")


def test_add_to_favorite(current_user, game):
    # Add the game to the user's favorite
    repo.add_to_user_favorite(current_user, game)

    # Check the final state of the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == [game]


def test_remove_from_favorite(current_user, game):
    # First add a game to the favorite list
    repo.add_to_user_favorite(current_user, game)

    # Then remove the game from the user's favorite list
    repo.remove_to_user_favorite(current_user, game)

    # Check the final state of the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_get_favorite_games(current_user, game):
    # Clear the favorite games list first
    for game_in_fav in repo.get_favs(current_user):
        repo.remove_to_user_favorite(current_user, game_in_fav)

    # Then add a game to the favorite list
    repo.add_to_user_favorite(current_user, game)

    # Get the favorite games list
    fav_games = repo.get_favs(current_user)

    # Check the final state of the favorite games list
    assert fav_games == [game]


def test_adding_duplicate_games(current_user, game):
    # Clear the favorite games list first
    for game_in_fav in repo.get_favs(current_user):
        repo.remove_to_user_favorite(current_user, game_in_fav)

    # Add the game to the user's favorite multiple times
    repo.add_to_user_favorite(current_user, game)
    repo.add_to_user_favorite(current_user, game)

    # Check that the game only appears once in the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == [game]


def test_removing_nonexistent_game(current_user, another_game):
    # Clear the favorite games list first
    for game_in_fav in repo.get_favs(current_user):
        repo.remove_to_user_favorite(current_user, game_in_fav)

    # Try to remove a game that is not in the favorite list
    repo.remove_to_user_favorite(current_user, another_game)

    # Check that no errors were raised and the favorite list is still empty
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_empty_favourites(current_user):
    # Clear the favorite games list first
    for game_in_fav in repo.get_favs(current_user):
        repo.remove_to_user_favorite(current_user, game_in_fav)

    # Check that the favorite games list is empty
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_multiple_users(current_user, game, another_game):
    # Create another user
    another_user = User(username="testuser2", password="password456")
    repo.add_user(another_user)
    another_user = repo.get_user("testuser2")

    # Add different games to each user's favorite list
    repo.add_to_user_favorite(current_user, game)
    repo.add_to_user_favorite(another_user, another_game)

    # Check that one user's favorite list does not show up in the other user's list
    current_user_fav_games = repo.get_favs(current_user)
    another_user_fav_games = repo.get_favs(another_user)

    assert game in current_user_fav_games
    assert another_game in another_user_fav_games
    assert game not in another_user_fav_games
    assert another_game not in current_user_fav_games


