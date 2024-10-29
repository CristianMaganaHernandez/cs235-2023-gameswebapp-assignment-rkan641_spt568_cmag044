from typing import List, Union

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game


def get_games_pagination(repo: AbstractRepository, genre="All", offset=0, limit=10, order_by='title'):
    return repo.get_games_pagination(genre, offset, limit, order_by)


def get_game_genres(repo: AbstractRepository) -> List[str]:
    return repo.get_game_genres()


def get_number_of_games_by_genre(repo: AbstractRepository, genre):
    return repo.get_number_of_games_by_genre(genre)


def get_games_by_genre(repo: AbstractRepository, selected_genre: str) -> [Game]:
    return repo.get_games_by_genre(selected_genre)
