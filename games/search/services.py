from typing import List

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game

def search_games( repo: AbstractRepository, query: str, filter_option: str, price_filter: list) -> List[Game]:
    return repo.search_games(query, filter_option, price_filter)