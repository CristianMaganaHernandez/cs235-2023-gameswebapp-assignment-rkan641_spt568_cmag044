from typing import List, Union

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game

def get_user(repo: AbstractRepository, username: str) -> Union[User, None]:
    return repo.get_user(username)
def get_wishlist(repo: AbstractRepository, username):
    return repo.get_wishlist(username)
def get_favs(repo: AbstractRepository, user):
    return repo.get_favs(user)