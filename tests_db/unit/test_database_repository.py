
import datetime

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Game, Publisher, User, Wishlist, Review, Genre, add_review
from games.adapters.repository import RepositoryException

def test_repository_get_number_of_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_number_of_games() == 878


def test_repository_add_game(session_factory):

    repo = SqlAlchemyRepository(session_factory)
    # Input correct class
    game = Game(999, "Test Game")
    game.price = 2.99
    game.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")
    repo.add_game(game)
    assert repo.get_number_of_games() == 879

    # Input incorrect class
    game2 = Publisher("Bethesda")
    repo.add_game(game2)
    assert repo.get_number_of_games() == 879


def test_repository_get_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games()

    # Check if repo.get_games() returns correct number of games
    assert len(games) == repo.get_number_of_games()

    # Check repo.get_games() returns list
    assert isinstance(games, list)

    # Check if repo contains a list of only Games classes
    assert all(isinstance(game, Game) for game in games)


def test_repository_add_multiple_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    games = repo.get_games()

    for game in [new_game1, new_game2, new_game3]:
        assert game in games


def test_repository_add_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_user = User("Bob", "test123")
    repo.add_user(new_user)

    # Correct username
    assert repo.get_user(new_user.username) == new_user

    # Incorrect username
    assert repo.get_user("afasfas") is None


def test_repository_service_returns_existing_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    results = repo.search_games('Game Title', 'Title', [])
    assert results == [game for game in repo.get_games() if 'Game Title' in game.title]


def test_repository_service_retrieves_correct_number_of_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.search_games('Game Title', 'Title', [])) == 0


def test_repository_getting_games_for_search_key_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    results = repo.search_games('Action', 'Genre', [])
    expected_games = [game for game in repo.get_games() if 'Action' in [genre.genre_name for genre in game.genres]]

    for game in expected_games:
        assert game in results


def test_repository_getting_games_for_search_key_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    results = repo.search_games('Acti', 'Publisher', [])
    assert results != []


def test_repository_inserting_non_existing_search_key_throws_exception(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.search_games('food', 'All', []) == []


def test_repository_getting_games_for_price(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    results = repo.search_games('a', 'Title', ["40-70"])
    assert results != []


def test_add_to_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    repo.add_to_user_wishlist(current_user, new_game3)

    # check the final state of the wishlist
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == [new_game3]


def test_remove_from_wishlist(session_factory):
    # first add a game to the wishlist
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    repo.add_to_user_wishlist(current_user, new_game3)

    # then remove the game from the user's wishlist
    repo.remove_from_user_wishlist(current_user, new_game3)

    # check the final state of the wishlist
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


def test_get_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    repo.add_to_user_wishlist(current_user, new_game3)


    # clear the wishlist first
    repo.remove_from_user_wishlist(current_user, new_game3)

    # then add a game to the wishlist
    repo.add_to_user_wishlist(current_user, new_game1)

    # get the wishlist
    wishlist = repo.get_wishlist(current_user)

    # check the final state of the wishlist
    assert wishlist == [new_game1]


def test_adding_duplicate_games_to_wishlist(session_factory):
    """Test adding duplicate games to the wishlist; the game should only appear once."""
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    # Adding the game to the wishlist twice
    repo.add_to_user_wishlist(current_user, new_game3)
    repo.add_to_user_wishlist(current_user, new_game3)

    # Retrieve the wishlist and check that the game appears only once
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == [new_game3]


def test_removing_non_existent_game(session_factory):
    """Test removing a non-existent game from the wishlist; it should not raise errors."""
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])
    # Trying to remove a game that was not added to the wishlist
    repo.remove_from_user_wishlist(current_user, new_game3)

    # Retrieve the wishlist and check that it is empty
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


def test_empty_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    repo.add_user(current_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    """Test retrieving an empty wishlist."""

    # Ensure the wishlist is empty
    wishlist = repo.get_wishlist(current_user)
    assert wishlist == []


def test_wishlist_with_multiple_users(session_factory):
    """Test that one user's wishlist games do not show up in another user's wishlist."""
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    # Add games to the wishlists of two different users
    repo.add_to_user_wishlist(current_user, new_game3)
    repo.add_to_user_wishlist(another_user, new_game1)

    # Check that the wishlists are separate
    wishlist_user1 = repo.get_wishlist(current_user)
    wishlist_user2 = repo.get_wishlist(another_user)

    assert wishlist_user1 == [new_game3]
    assert wishlist_user2 == [new_game1]



def test_add_to_favorite(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    # Add the game to the user's favorite
    repo.add_to_user_favorite(current_user, new_game3)

    # Check the final state of the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == [new_game3]

def test_remove_from_favorite(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])
    # First add a game to the favorite list
    repo.add_to_user_favorite(current_user, new_game3)

    # Then remove the game from the user's favorite list
    repo.remove_to_user_favorite(current_user, new_game3)

    # Check the final state of the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_adding_duplicate_games_to_favorites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])
    # First add a game to the favorite list
    repo.add_to_user_favorite(current_user, new_game3)

    # Add the game to the user's favorite multiple times
    repo.add_to_user_favorite(current_user, new_game3)
    repo.add_to_user_favorite(current_user, new_game3)

    # Check that the game only appears once in the favorite games list
    fav_games = repo.get_favs(current_user)
    assert fav_games == [new_game3]


def test_removing_nonexistent_game_from_favorites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])

    # Try to remove a game that is not in the favorite list
    repo.remove_to_user_favorite(current_user, new_game3)

    # Check that no errors were raised and the favorite list is still empty
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_empty_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])
    # First add a game to the favorite list

    # Check that the favorite games list is empty
    fav_games = repo.get_favs(current_user)
    assert fav_games == []


def test_favorites_with_multiple_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    current_user = User("YOZA", "test123")
    another_user = User("MATA", "test123")
    repo.add_user(current_user)
    repo.add_user(another_user)

    new_game1 = Game(0, "Test Game 1")
    new_game1.price = 2.99
    new_game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    new_game2 = Game(99999999, "Test Game 2")
    new_game2.price = 5.99
    new_game2.release_date = datetime.date(2022, 11, 18).strftime("%b %d, %Y")

    new_game3 = Game(435791, "Test Game 3")
    new_game3.price = 12.99
    new_game3.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")

    repo.add_multiple_games([new_game1, new_game2, new_game3])
    # First add a game to the favorite list
    repo.add_to_user_favorite(current_user, new_game3)
    repo.add_to_user_favorite(another_user, new_game1)

    # Check that one user's favorite list does not show up in the other user's list
    current_user_fav_games = repo.get_favs(current_user)
    another_user_fav_games = repo.get_favs(another_user)

    assert current_user_fav_games == [new_game3]
    assert another_user_fav_games == [new_game1]


def test_add_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # User and game already inserted into session in conf test
    user = repo.get_user("Cris")
    game = repo.get_game(5121)

    review = add_review("I like", 4, game, user)
    repo.add_review(review)

    assert len(repo.get_reviews()) == 1

    assert review in repo.get_reviews()


def test_add_multiple_reviews_to_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # User and game already inserted into session in conf test
    user = repo.get_user("Cris")
    game = repo.get_game(5121)

    review = add_review("I like", 4, game, user)
    review2 = add_review("Mid", 5, game, user)
    repo.add_review(review)
    repo.add_review(review2)

    result = repo.get_reviews()

    assert len(result) == 2

    assert review in result
    assert review2 in result


def test_repository_search_games_by_title(session_factory):
    # Given a repository with predefined games
    repo = SqlAlchemyRepository(session_factory)

    # Add games to the repository
    game1 = Game(3010, "Xpand Rally")  # Unique game_id = 3010
    game1.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")
    game1.price = 5.99
    repo.add_game(game1)

    game2 = Game(2, "Cool Game2")  # Unique game_id = 2
    game2.release_date = datetime.date(1998, 11, 18).strftime("%b %d, %Y")
    game2.price = 9.00
    repo.add_game(game2)

    # When a game is searched by title
    games = repo.search_games_by_title("Cool Game2")

    # Then the correct game should be returned
    assert games is not None, "Expected a list but got None."
    assert len(games) == 1  # Expecting only 1 match
    assert games[0].title == "Cool Game2"


def test_repository_search_games_by_publisher(session_factory):
    # Given a repository with predefined games
    repo = SqlAlchemyRepository(session_factory)

    # Add a game with a publisher to the repository
    game = Game(1001, "Action Game")
    publisher = Publisher("Epic Games")
    game.publisher = publisher
    game.release_date = datetime.date(2015, 8, 25).strftime("%b %d, %Y")
    game.price = 5.77  # Setting a default value

    repo.add_game(game)

    # When games are searched by publisher with no price filter
    games = repo.search_games("Epic Games", "Publisher", [])

    # Then the correct game(s) should be returned
    assert len(games) == 1
    assert games[0].publisher.publisher_name == "Epic Games"


def test_repository_search_games_by_genre(session_factory):
    # Given a repository with predefined games
    repo = SqlAlchemyRepository(session_factory)

    # Add a game with a genre to the repository
    game = Game(1002, "Fantasy Game")
    genre = Genre("Fantasy")
    game.add_genre(genre)
    game.release_date = datetime.date(2018, 10, 10).strftime("%b %d, %Y")
    game.price = 1.66  # Setting a default value
    repo.add_game(game)

    # When games are searched by genre with a price filter
    games = repo.search_games("Fantasy", "Genre", ["0-10"])

    # Then the correct game(s) should be returned
    assert len(games) == 1
    assert "Fantasy" in [genre.genre_name for genre in games[0].genres]


def test_repository_search_games_by_release_year(session_factory):
    # Given a repository with predefined games
    repo = SqlAlchemyRepository(session_factory)

    # Add a game to the repository
    game = Game(1003, "Modern Game")
    game.release_date = datetime.date(2021, 1, 1).strftime("%b %d, %Y")
    game.price = 6.99  # Setting a default value
    repo.add_game(game)

    # When games are searched by release year with no price filter
    games = repo.search_games("2021", "Release Year", [])

    # Then the correct game(s) should be returned
    assert len(games) == 176
    assert "2021" in games[0].release_date
