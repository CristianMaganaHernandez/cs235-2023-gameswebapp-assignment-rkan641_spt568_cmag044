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


def test_add_to_wishlist(current_user, game):
    # add the game to the user's wishlist
    repo.add_to_user_wishlist(current_user, game)

    # check the final state of the wishlist
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == [game]


def test_remove_from_wishlist(current_user, game):
    # first add a game to the wishlist
    repo.add_to_user_wishlist(current_user, game)

    # then remove the game from the user's wishlist
    repo.remove_from_user_wishlist(current_user, game)

    # check the final state of the wishlist
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


def test_get_wishlist(current_user, game):
    # clear the wishlist first
    repo.remove_from_user_wishlist(current_user, game)

    # then add a game to the wishlist
    repo.add_to_user_wishlist(current_user, game)

    # get the wishlist
    wishlist = repo.get_wishlist(current_user)

    # check the final state of the wishlist
    assert wishlist == [game]


def test_adding_duplicate_games(current_user, game):
    """Test adding duplicate games to the wishlist; the game should only appear once."""

    # Adding the game to the wishlist twice
    repo.add_to_user_wishlist(current_user, game)
    repo.add_to_user_wishlist(current_user, game)

    # Retrieve the wishlist and check that the game appears only once
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == [game]


def test_removing_non_existent_game(current_user, game):
    """Test removing a non-existent game from the wishlist; it should not raise errors."""

    # Trying to remove a game that was not added to the wishlist
    repo.remove_from_user_wishlist(current_user, game)

    # Retrieve the wishlist and check that it is empty
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


def test_empty_wishlist(current_user):
    """Test retrieving an empty wishlist."""

    # Ensure the wishlist is empty
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


@pytest.fixture
def another_user():
    user = User(username="anotheruser", password="password456")
    repo.add_user(user)
    return user


def test_multiple_users(current_user, another_user, game, another_game):
    """Test that one user's wishlist games do not show up in another user's wishlist."""

    # Add games to the wishlists of two different users
    repo.add_to_user_wishlist(current_user, game)
    repo.add_to_user_wishlist(another_user, another_game)

    # Check that the wishlists are separate
    wishlist_user1 = repo.get_wishlist(current_user)
    wishlist_user2 = repo.get_wishlist(another_user)

    assert wishlist_user1 == [game]
    assert wishlist_user2 == [another_game]

