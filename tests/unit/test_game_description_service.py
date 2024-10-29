from unittest.mock import Mock, patch
import pytest
from games.adapters.memory_repository import MemoryRepository, populate2
from games.domainmodel.model import User
from games.game_description.game_description import submit_review, game_description_blueprint
from games.game_description.services import get_game_by_id



def test_get_game_by_id():

    repo = MemoryRepository()
    populate2(repo)

    # Test Valid Ids
    assert get_game_by_id(repo, 435790).title == "10 Second Ninja X"
    assert get_game_by_id(repo, 1000040).title == "细胞战争"

    # Test Invalid Ids
    assert get_game_by_id(repo, 0) is None
    assert get_game_by_id(repo, 999999999999) is None
    assert get_game_by_id(repo, '5jpaosjft') is None
    assert get_game_by_id(repo, [1, 2, 3]) is None


from unittest.mock import patch
from games.domainmodel.model import User

def test_submit_review(client, memory_repo):
    # Set up the repository, populate it, and create a user
    user = User("testuser", "password")
    memory_repo.add_user(user)

    # Create a review
    game_id = 435790  # Replace with a valid game ID
    rating = 4
    comment = "Great game!"
    game_title = "10 Second Ninja X"

    # Get the game before submitting the review
    game_before_review = get_game_by_id(memory_repo, game_id)

    # Use the client fixture to create a request context
    with client.application.test_request_context(f'/submit_review/{game_id}/{game_title}', method='POST'):
        # Mock session data
        with patch.dict('flask.session', {'user_name': 'testuser'}, clear=True):
            # Mock the request form
            with patch('flask.request.form', {'rating': str(rating), 'comment': comment}):
                # Use the client to invoke the route
                response = client.post(f'/submit_review/{game_id}/{game_title}')
                assert response.status_code == 302

def test_submit_review2(client, memory_repo):
    # Similar setup as test_submit_review, but you can vary the details to test different conditions.
    user = User("testuser2", "password")
    memory_repo.add_user(user)

    game_id = 435790
    rating = 5
    comment = "Fantastic game!"
    game_title = "10 Second Ninja X"

    game_before_review = get_game_by_id(memory_repo, game_id)

    # Use the client fixture to create a request context
    with client.application.test_request_context(f'/submit_review/{game_id}/{game_title}', method='POST'):
        # Mock session data
        with patch.dict('flask.session', {'user_name': 'testuser2'}, clear=True):
            # Mock the request form
            with patch('flask.request.form', {'rating': str(rating), 'comment': comment}):
                # Use the client to invoke the route
                response = client.post(f'/submit_review/{game_id}/{game_title}')
                assert response.status_code == 302
