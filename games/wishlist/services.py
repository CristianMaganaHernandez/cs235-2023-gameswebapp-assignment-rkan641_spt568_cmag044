from typing import List, Union

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game


def get_game_by_id(repo: AbstractRepository, game_id: int):
    return repo.get_game_by_id(game_id)

def get_user(repo: AbstractRepository, username) -> Union[User, None]:
    return repo.get_user(username)

def add_to_user_wishlist(repo: AbstractRepository, user: User, game: Game):
    return repo.add_to_user_wishlist(user, game)

def remove_from_user_wishlist(repo: AbstractRepository, user: User, game: Game):
    return repo.remove_from_user_wishlist(user, game)



def get_wishlist(repo: AbstractRepository, user: User):
    return repo.get_wishlist(user)
