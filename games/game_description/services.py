from typing import List, Union

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game
from games.domainmodel.model import add_review as add_rev


def calculate_average_rating(repo: AbstractRepository, game_id, reviews):
    # Adjust the below line according to how you handle the game_id and reviews
    return repo.calculate_average_rating(game_id, reviews)



def get_game_by_id(repo: AbstractRepository, game_id: int):
    return repo.get_game_by_id(game_id)


def get_user(repo: AbstractRepository, username: str) -> Union[User, None]:
    return repo.get_user(username)


def add_review(repo: AbstractRepository, comment: str, rating: int, game: Game, currentuser: User):
    return repo.add_review(add_rev(comment, rating, game, currentuser))

