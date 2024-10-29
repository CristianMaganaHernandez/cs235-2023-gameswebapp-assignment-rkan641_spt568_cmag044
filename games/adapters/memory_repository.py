import os
from bisect import insort_left
from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Review, Wishlist, Publisher, Genre
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from typing import List, Union


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__users = dict()
        self.__reviews = list()
        self.__user_wishlists = {}
        self.__fav_games = {}

    # WISHLIST

    def get_wishlist(self, user):
        if user.username in self.__user_wishlists:
            return self.__user_wishlists[user.username].list_of_games()
        else:
            return []

    def add_to_user_wishlist(self, user, game):
        if user.username in self.__user_wishlists:
            wishlist = self.__user_wishlists[user.username]

            if game not in wishlist.list_of_games():
                wishlist.add_game(game)
                print(f"Game {game} successfully added to {user.username}'s wishlist")  # New debug print
        else:
            wishlist = Wishlist(user)
            wishlist.add_game(game)
            self.__user_wishlists[user.username] = wishlist
            print(f"Game {game} successfully added to a new wishlist for {user.username}")  # New debug print

    def remove_from_user_wishlist(self, user, game):
        if user.username in self.__user_wishlists:
            self.__user_wishlists[user.username].remove_game(game)

    def add_to_user_favorite(self, user, game):
        if user.username in self.__fav_games:
            user_fav_games = self.__fav_games[user.username]
            if game not in user_fav_games:
                user_fav_games.append(game)
        else:
            self.__fav_games[user.username] = [game]

    def remove_to_user_favorite(self, user, game):
        if user.username in self.__fav_games:
            user_fav_games = self.__fav_games[user.username]
            if game in user_fav_games:
                user_fav_games.remove(game)

    # Games ------------------------------------
    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_favs(self, user):
        if user.username in self.__fav_games:
            return self.__fav_games[user.username]
        return []

    def get_number_of_games(self):
        return len(self.__games)

    # Auth -------------------------------------

    def add_user(self, user: User):
        if isinstance(user, User):
            self.__users.update({user.username: user})

    def get_user(self, username: str) -> Union[User, None]:
        if username in self.__users.keys():
            return self.__users[username]

    def add_review(self, review) -> Review:
        if isinstance(review, Review):
            insort_left(self.__reviews, review)

    def get_game_by_id(self, game_id: int):
        for game in self.__games:
            if game.game_id == game_id:
                return game


# NEW TESTING FOR CHANGES TO MEMORY REPO
    def search_games(self, query: str, filter_option: str, price_filter: list) -> List[Game]:
        games = self.__games
        filtered_games = []

        for game in games:
            if (query.lower() in game.title.lower() or
                    query.lower() in game.publisher.publisher_name.lower() or
                    query.lower() in [genre.genre_name.lower() for genre in game.genres] or query.isdigit()):

                if filter_option == 'Title':
                    if query.lower() in game.title.lower():
                        filtered_games.append(game)
                elif filter_option == 'Genre':
                    if any(genre.genre_name.lower() == query.lower() for genre in game.genres):
                        filtered_games.append(game)
                elif filter_option == 'Publisher':
                    if query.lower() in game.publisher.publisher_name.lower():
                        filtered_games.append(game)
                elif filter_option == 'Release Year':
                    year_list = game.release_date.split()
                    year = year_list[-1]
                    if int(query) == int(year):
                        filtered_games.append(game)

        if price_filter:
            filtered_by_price = []
            for price_range in price_filter:
                a_list = price_range.split('-')
                min_price = int(a_list[0])
                max_price = int(a_list[1])
                for game in filtered_games:
                    if min_price <= game.price <= max_price:
                        filtered_by_price.append(game)
            return filtered_by_price

        return filtered_games

    def calculate_average_rating(self, game_id,reviews):
        if not reviews:
            return 0.0  # Return 0 if there are no reviews
        if isinstance(reviews, (list, tuple)):
            total_rating = sum(review.rating for review in reviews)
        else:
            total_rating = 0  # or any other appropriate default value

        if isinstance(reviews, (list, tuple)):
            num_reviews = len(reviews)
        else:
            num_reviews = 0  # or any other appropriate default value

        if num_reviews == 0:
            return None  # or return 0 or any other appropriate value

        return total_rating / num_reviews

    def get_games_pagination(self, genre="All", offset=0, limit=10, order_by='title'):

        games = self.get_games_by_genre(genre)
        sorted_games = sorted(games, key=lambda x: getattr(x, order_by, ""))

        paginated_games = sorted_games[offset:offset + limit]

        game_dicts = []
        for game in paginated_games:
            game_dict = {
                "game_id": game.game_id,
                "title": game.title,
                "release_date": game.release_date
            }
            game_dicts.append(game_dict)

        return game_dicts

    # Should I put this in memory repository instead?
    def get_games_by_genre(self, selected_genre: str) -> [Game]:
        games = self.__games
        if selected_genre == "All":
            return games

        valid_games = []
        for game in games:
            for genre in game.genres:
                if selected_genre == genre.genre_name:
                    valid_games.append(game)
        return valid_games

    def get_number_of_games_by_genre(self, genre):
        return len(self.get_games_by_genre(genre))

    def get_game_genres(self) -> List[str]:
        # flatten 3d list into 2d set
        all_genres = []
        for game in self.__games:
            for genre in game.genres:
                all_genres.append(genre.genre_name)

        # set return will cause error
        all_genres = sorted(set(all_genres))
        return all_genres

    def add_multiple_games(self, games: List[Game]):
        pass
    def add_multiple_genres(self, genres: List[Genre]):
        pass
    def add_multiple_publishers(self, publisher: List[Publisher]):
        pass
    def add_publisher(self, publisher: Publisher):
        pass
    def get_game(self, game_id: int) -> Game:
        pass
    def get_genres(self, genre: Genre) -> List[Genre]:
        pass
    def get_number_of_publishers(self):
        pass
    def get_publishers(self) -> List[Publisher]:
        pass
    def search_games_by_title(self, title_string: str) -> List[Game]:
        pass
    def get_reviews(self):
        pass


def load_games(repo: AbstractRepository, data_path: Path = None):

    # Current fallback otherwise a lot of things will fail
    if data_path is None:
        dir_name = os.path.dirname(os.path.abspath(__file__))
        games_file_name = os.path.join(dir_name, "data/games.csv")
    else:
        games_file_name = str(Path(data_path) / "games.csv")

    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()

    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)


def populate2(repo: AbstractRepository, data_path: Path = None):
    load_games(repo, data_path)



