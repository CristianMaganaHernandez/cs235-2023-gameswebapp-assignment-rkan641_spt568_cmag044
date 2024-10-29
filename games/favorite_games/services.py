from typing import List, Union

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game

def get_game_by_id(repo: AbstractRepository, game_id: int):
    return repo.get_game_by_id(game_id)

def get_user(repo: AbstractRepository, username: str) -> Union[User, None]:
    return repo.get_user(username)

def add_to_user_favorite(repo: AbstractRepository,user, game):
    return repo.add_to_user_favorite(user, game)

def remove_to_user_favorite(repo: AbstractRepository, user, game):
    return repo.remove_to_user_favorite(user, game)
