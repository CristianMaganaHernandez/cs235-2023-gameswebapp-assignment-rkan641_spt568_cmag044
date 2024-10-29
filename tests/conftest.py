
import pytest

from games import create_app
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository

from pathlib import Path

from games.domainmodel.model import User

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing

project_root = Path(__file__).parent

TEST_DATA_PATH = project_root / "data"


@pytest.fixture
def memory_repo():
    repo = MemoryRepository()
    memory_repository.populate2(repo, TEST_DATA_PATH)

    # Add a user with username 'user1' to the repository
    user1 = User('user1', 'Attentiveshout3968')  # You can use the actual password here
    repo.add_user(user1)

    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False,                       # test_client will not send a CSRF token, so disable validation.
        'REPOSITORY': 'memory'
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='user1', password='Attentiveshout3968'):
        return self.__client.post(
            'authentication/login',
            data={'username': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
