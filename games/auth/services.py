

from argon2 import PasswordHasher

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def user_to_dict(user: User):
    user_dict = {
        'user_name': user.username,
        'password': user.password
    }
    return user_dict


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


# For Argon2 encryption
ph = PasswordHasher()


def add_user(username: str, password: str, repo: AbstractRepository):

    # Check that the given username is available.
    user = repo.get_user(username)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password
    password_hash = ph.hash(password)

    # Create and store the new User, with password encrypted.
    user = User(username, password_hash)
    repo.add_user(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)

    if user is not None:
        try:
            authenticated = ph.verify(user.password, password)
        except Exception:
            raise AuthenticationException

    if not authenticated:
        raise AuthenticationException

