from abc import ABC
from typing import List, Type
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.elements import or_, and_

from games.adapters.orm import reviews_table, game_genres_table, user_wishlist_table
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Publisher, Genre, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # This method can be used to start a new session for each HTTP request, e.g., in a Flask app.
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            session = self._session_cm
            try:
                session.session.merge(game)
                session.commit()
            except IntegrityError:
                # This error is raised if a duplicate entry is added, for example.
                # You can handle this or any other database-specific errors as needed.
                session.rollback()
                raise
            finally:
                session.session.close()


    def get_wishlist(self, user: User) -> List[Game]:
        return user._User__wishlist

    def add_to_user_wishlist(self, user: User, game: Game):
        # Use SQLAlchemy to get the user object from the database based on the username.
        user_from_db = self.get_user(user.username)

        if user_from_db:
            # Check if the game exists in the database
            game_from_db = self.get_game_by_id(game._Game__game_id)

            if not game_from_db:
                print(f"Game {game} not found in the database.")  # New debug print
                return

            # Check if the game is not already in the user's wishlist
            if game_from_db not in user_from_db._User__wishlist:
                # Explicitly create a new association for user_wishlist_table
                new_wishlist_item = user_wishlist_table.insert().values(
                    user_id=user_from_db._User__user_id,
                    game_id=game_from_db._Game__game_id
                )
                with self._session_cm as scm:
                    scm.session.execute(new_wishlist_item)
                    scm.commit()
                print(f"Game {game} successfully added to {user.username}'s wishlist")  # New debug print
            else:
                print(f"Game {game} is already in {user.username}'s wishlist")  # New debug print
        else:
            print(f"User {user.username} not found in the database.")  # New debug print

    def remove_from_user_wishlist(self, user, game):
        # Get the user object from the database.
        user_from_db = self.get_user(user.username)

        if user_from_db:
            # Check if the game is in the user's wishlist.
            if game in user_from_db._User__wishlist:
                # Remove the game from the user's wishlist.
                user_from_db._User__wishlist.remove(game)

                with self._session_cm as scm:
                    scm.session.add(user_from_db)
                    scm.commit()

    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_User__username=username).one()
        except NoResultFound:
            pass
        return user

    def add_review(self, review: Review) -> Review:
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_game_by_id(self, game_id: int):
        game = None
        try:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            pass
        return game

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def get_publishers(self) -> List[Publisher]:
        pass

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        pass


    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games

    def add_to_user_favorite(self, user: User, game: Game):
        # Use SQLAlchemy to get the user object from the database based on the username.
        user_from_db = self.get_user(user.username)

        if user_from_db:
            # Check if the game exists in the database
            game_from_db = self.get_game_by_id(game._Game__game_id)

            if not game_from_db:
                print(f"Game {game} not found in the database.")
                return

            # Check if the game is not already in the user's favorite games
            if game_from_db not in user_from_db._User__favourite_games:
                # Assuming that you have a relationship between User and Game for favorite games,
                # you can simply add the game to the user's favorite games list.
                user_from_db._User__favourite_games.append(game_from_db)

                with self._session_cm as scm:
                    scm.commit()
                print(f"Game {game} successfully added to {user.username}'s favorite games")
            else:
                print(f"Game {game} is already in {user.username}'s favorite games")
        else:
            print(f"User {user.username} not found in the database.")

    def remove_to_user_favorite(self, user, game):
        user_from_db = self.get_user(user.username)
        if user_from_db:
            if game in user_from_db._User__favourite_games:
                user_from_db._User__favourite_games.remove(game)
                with self._session_cm as scm:
                    scm.session.add(user)
                    scm.commit()

    def get_genres(self) -> List[Genre]:
        pass

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    def search_games_by_title(self, title_string: str) -> List[Game]:
        session = self._session_cm.session
        games = session.query(Game).filter(Game._Game__game_title.ilike(f"%{title_string}%")).all()
        return games

    def get_favs(self, user: User) -> List[Game]:
        # Ensure that the user is loaded with their favorite games.
        self._session_cm.session.refresh(user)

        # Access the favorite games directly from the loaded user object.
        return user.favourite_games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def get_number_of_games_by_genre(self, genre):
        games = self.get_games_by_genre(genre)
        return len(games)

    def get_game_genres(self) -> List[str]:
        unique_genres = (
            self._session_cm.session.query(Genre._Genre__genre_name)
            .distinct()
            .order_by(Genre._Genre__genre_name)
            .all()
        )
        all_genres = [genre[0] for genre in unique_genres]
        return all_genres

    def get_games_by_genre(self, selected_genre: str) -> List[Game]:
        with self._session_cm as session_manager:
            if selected_genre == "All":
                games = (
                    session_manager.session.query(Game)
                    .order_by(Game._Game__game_id)
                    .all()
                )
            else:
                games = (
                    session_manager.session.query(Game)
                    .join(game_genres_table)  # join with game_genres table
                    .join(Genre, Genre._Genre__genre_name == game_genres_table.c.genre_name)  # join with genres
                    .filter(Genre._Genre__genre_name == selected_genre)
                    .order_by(Game._Game__game_id)
                    .all()
                )
            return games

    def get_games_pagination(self, genre="All", offset=0, limit=10, order_by='title'):
        session = self._session_cm.session

        # If the genre is "All", we don't filter by genre
        if genre == "All":
            query = session.query(Game)
        else:
            query = (session.query(Game)
                     .join(game_genres_table)  # join with game_genres table
                     .join(Genre, Genre._Genre__genre_name == game_genres_table.c.genre_name)  # join with genres
                     .filter(Genre._Genre__genre_name == genre))

        # Sort the query results
        query = query.order_by(
            getattr(Game, '_Game__' + order_by))  # Adjusted this line to filter based on Game's attributes

        # Apply offset and limit
        paginated_games = query.offset(offset).limit(limit).all()

        game_dicts = [{
            "game_id": game._Game__game_id,
            "title": game._Game__game_title,
            "release_date": game._Game__release_date
        } for game in paginated_games]

        session.close()

        return game_dicts

    def calculate_average_rating(self, game_id, reviews):
        session = self._session_cm.session

        average_rating = session.query(func.avg(reviews_table.c.rating)) \
            .filter(reviews_table.c.game_id == game_id) \
            .scalar()

        if average_rating is None:
            return 0.0
        return round(average_rating, 1)

    def search_games(self, query: str, filter_option: str, price_filter: list) -> List[Game]:
        # Use session from the context manager
        games_query = self._session_cm.session.query(Game).options(
            joinedload(Game._Game__genres),
            joinedload(Game._Game__publisher)
        )

        if filter_option == 'Title':
            games_query = games_query.filter(Game._Game__game_title.ilike(f"%{query}%"))
        elif filter_option == 'Genre':
            games_query = games_query.join(Game._Game__genres).filter(Genre._Genre__genre_name.ilike(f"%{query}%"))
        elif filter_option == 'Publisher':
            games_query = games_query.join(Game._Game__publisher).filter(Publisher._Publisher__publisher_name.ilike(f"%{query}%"))
        elif filter_option == 'Release Year' and query.isdigit():
            year = int(query)
            # If release_date is a string:
            games_query = games_query.filter(Game._Game__release_date.like(f"% {year}"))
            # If release_date is a date object:
            # games_query = games_query.filter(func.extract('year', Game._Game__release_date) == year)
        else:
            # Invalid filter option
            return []


        if price_filter:
            price_conditions = []
            for price_range in price_filter:
                min_price, max_price = map(int, price_range.split('-'))
                price_conditions.append(and_(Game._Game__price >= min_price, Game._Game__price <= max_price))
            games_query = games_query.filter(or_(*price_conditions))

        return games_query.all()

    def get_reviews(self) -> List[Type[Review]]:
        session = self._session_cm.session

        # Query the reviews from the database
        reviews = session.query(Review).all()

        return reviews

