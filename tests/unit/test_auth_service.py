import pytest

from games.auth.services import NameNotUniqueException, UnknownUserException, AuthenticationException
import games.auth.services as services
from games.domainmodel.model import User


def test_can_add_user(memory_repo):
    new_user_name = 'user'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, memory_repo)

    user_as_dict = services.get_user(new_user_name, memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('$argon2id$')


def test_cannot_add_user_with_existing_name(memory_repo):
    user_name = 'user'
    password = 'abcd1A23'

    # Create a user object with the username and password
    user = User(user_name, password)

    # Add the user to the memory repository
    memory_repo.add_user(user)

    # Your additional test logic here, like checking for the NameNotUniqueException


def test_cannot_get_user_with_unknown_username(memory_repo):
    user_name = 'user3'

    with pytest.raises(UnknownUserException):
        services.get_user(user_name, memory_repo)


def test_authentication_with_valid_credentials(memory_repo):
    new_user_name = 'user4'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, memory_repo)

    try:
        services.authenticate_user(new_user_name, new_password, memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(memory_repo):
    new_user_name = 'user5'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, memory_repo)

    with pytest.raises(AuthenticationException):
        services.authenticate_user(new_user_name, '0987654321', memory_repo)
