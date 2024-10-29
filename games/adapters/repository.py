import abc
from typing import List

from games.domainmodel.model import Game, User, Genre, Publisher, Review

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    def get_wishlist(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review) -> Review:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_user_wishlist(self, username: str, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_user_wishlist(self, username: str, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_user_favorite(self,user, game):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_to_user_favorite(self, user, game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_favs(self, user):
        raise NotImplementedError

#NEW STUFF FOR TESTING FROM HERE ONWARDS
    def search_games(self, query: str, filter_option: str, price_filter: list) -> List[Game]:
        raise NotImplementedError

    def calculate_average_rating(self, game_id, reviews):
        raise NotImplementedError

    def get_games_pagination(self, genre="All", offset=0, limit=10, order_by='title'):
        raise NotImplementedError

    def get_games_by_genre(self, selected_genre: str) -> [Game]:
        raise NotImplementedError

    def get_number_of_games_by_genre(self, genre):
        raise NotImplementedError

    def get_game_genres(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_genres(self, genres: List[Genre]):
        """ Add many genres to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_games(self, games: List[Game]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_publishers(self, publisher: List[Publisher]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        """ Add a single game to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> List[Publisher]:
        """ Returns the list of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_publishers(self):
        """ Returns a number of games exist in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int) -> Game:
        """ Returns the list of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_games_by_title(self, title_string: str) -> List[Game]:
        """Search for the games whose title includes the parameter title_string.
        It searches for the game title in case-insensitive and without trailing space.
        For example, the title 'Call of Duty' will be searched if the title_string is 'duty'. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self, genre: Genre) -> List[Genre]:
        """ Return all genres that exist in the repository. """
        raise NotImplementedError

    def get_reviews(self):
        raise NotImplementedError
