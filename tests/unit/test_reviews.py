from unittest.mock import Mock

import pytest
from pathlib import Path
from games.domainmodel.model import Game, User, Review, Wishlist
from games.adapters.memory_repository import MemoryRepository, populate2 as populate, load_games
from games.game_description.services import calculate_average_rating


# Fixtures to initialize objects for testing
@pytest.fixture
def mock_reviews():
    # Mocking a list of reviews with ratings
    return [Mock(rating=3), Mock(rating=4), Mock(rating=5)]

@pytest.fixture
def user():
    return User(username="testuser", password="password123")

@pytest.fixture
def game():
    return Game(game_id=1, game_title="Test Game")

@pytest.fixture
def review(user, game):
    return Review(user=user, game=game, rating=3, comment="Good Game")

# Test cases


def test_add_user(memory_repo, user):
    memory_repo.add_user(user)
    assert memory_repo.get_user(user.username) == user


def test_add_game(memory_repo, game):
    initial_game_count = memory_repo.get_number_of_games()
    memory_repo.add_game(game)
    assert memory_repo.get_number_of_games() == initial_game_count + 1


def test_get_game_by_id(memory_repo, game):
    memory_repo.add_game(game)
    assert memory_repo.get_game_by_id(game.game_id) == game


def test_add_review(memory_repo, review):
    # Add the review to the repository
    memory_repo.add_review(review)

    # Verify that the review has been added to the repository
    assert review in memory_repo._MemoryRepository__reviews

    # Additional assertions to check the state of the repository
    assert len(memory_repo._MemoryRepository__reviews) == 1  # Check the number of reviews
    assert memory_repo._MemoryRepository__reviews[0] == review  # Check if the added review is the same as the first review in the list


def test_submit_review(memory_repo, user, game):
    # Add the user and game to the repository
    memory_repo.add_user(user)
    memory_repo.add_game(game)

    # Call the submit_review function
    review = Review(user=user, game=game, rating=4, comment="Great Game")
    memory_repo.add_review(review)

    # Verify that the review has been added to the repository
    assert review in memory_repo._MemoryRepository__reviews

    # Additional assertions to check the state of the repository
    assert len(memory_repo._MemoryRepository__reviews) == 1  # Check the number of reviews
    assert memory_repo._MemoryRepository__reviews[0] == review  # Check if the added review is the same as the first review in the list


def test_average_rating_with_reviews(mock_reviews):
    # Create a mock repository with a calculate_average_rating method that accepts two arguments
    mock_repo = Mock(calculate_average_rating=lambda game_id, reviews: sum(review.rating for review in reviews) / len(reviews))

    # Call the calculate_average_rating function with the mock repository and mock reviews
    average_rating = calculate_average_rating(mock_repo, 1, mock_reviews)  # Pass game_id as the first argument

    # Calculate the expected average rating manually
    expected_average = (3 + 4 + 5) / 3

    # Assert that the calculated average rating matches the expected value
    assert average_rating == expected_average



def test_average_rating_with_empty_reviews():
    # Create a mock repository with a calculate_average_rating method that accepts two arguments and handles empty list case
    mock_repo = Mock(calculate_average_rating=lambda game_id, reviews: sum(review.rating for review in reviews) / len(reviews) if reviews else 0.0)

    # Call the calculate_average_rating function with the mock repository and an empty list of reviews
    average_rating = calculate_average_rating(mock_repo, 1, [])  # Pass game_id as the first argument

    # Assert that the average rating is 0.0 for an empty list of reviews
    assert average_rating == 0.0



def test_review_with_minimum_rating(memory_repo, user, game):
    review = Review(user=user, game=game, rating=1, comment="Bad Game")
    memory_repo.add_review(review)

    assert memory_repo._MemoryRepository__reviews[0].rating == 1


def test_review_with_maximum_rating(memory_repo, user, game):
    review = Review(user=user, game=game, rating=5, comment="Excellent Game")
    memory_repo.add_review(review)

    assert memory_repo._MemoryRepository__reviews[0].rating == 5


def test_review_with_invalid_rating(memory_repo, user, game):
    with pytest.raises(ValueError):
        review = Review(user=user, game=game, rating=6, comment="Invalid Rating")
        memory_repo.add_review(review)


def test_empty_string_as_review_comment(memory_repo, user, game):
    review = Review(user=user, game=game, rating=4, comment="")
    memory_repo.add_review(review)

    assert memory_repo._MemoryRepository__reviews[0].comment == ""


def test_add_review_without_user_or_game(memory_repo, user, game):
    with pytest.raises(ValueError):
        review = Review(user=None, game=game, rating=4, comment="No user")
        memory_repo.add_review(review)

    with pytest.raises(ValueError):
        review = Review(user=user, game=None, rating=4, comment="No game")
        memory_repo.add_review(review)
