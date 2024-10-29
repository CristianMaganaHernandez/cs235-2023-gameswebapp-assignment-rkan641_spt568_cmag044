import pytest

import datetime

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Game, Review, User, Genre, Publisher, add_review


def insert_user(empty_session, values=None):
    new_name = "AttentiveShout"
    new_password = "Testing123"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute(text('INSERT INTO users (username, password) VALUES (:username, :password)'),
                          {'username': new_name, 'password': new_password})
    user_key = empty_session.execute(text('SELECT user_id FROM users WHERE username = :username'),
                                {'username': new_name}).fetchone()
    return user_key


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (username, password) VALUES (:username, :password)'),
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute(text('SELECT user_id FROM users')).mappings().all())
    keys = tuple(row["user_id"] for row in rows)
    return keys


def make_user():
    user = User("YearningShout", "123Testing")
    return user


def insert_publisher(empty_session):
    publisher_name = "FromSoftware, Inc"

    empty_session.execute(text('INSERT INTO publishers (name) VALUES (:publisher_name)'),
                          {"publisher_name": publisher_name})

    publisher = empty_session.execute(text('SELECT name FROM publishers WHERE name = :publisher_name'),
                                     {'publisher_name': publisher_name}).mappings().one()

    return publisher["name"]


def make_publisher():
    return Publisher("FromSoftware, Inc")


def insert_game(empty_session):
    release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    game_title = "Minecraft"

    empty_session.execute(text(
        'INSERT INTO games (game_id, game_title, game_price, release_date) VALUES'
        '(1234, :game_title, 29.99, :date)'),
        {"game_title": game_title, "date": release_date}
    )

    game_key = empty_session.execute(text('SELECT game_id FROM games WHERE game_title = :game_title'),
                                     {'game_title': game_title}).mappings().one()

    return game_key["game_id"]


def make_game():
    release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    game = Game(1234, "Minecraft")
    game.release_date = release_date
    game.price = 29.99
    # game.publisher = Publisher("Mojang")

    return game


def insert_game_publisher_association(empty_session):
    release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    game1_title = "Minecraft"
    game2_title = "Minecraft Earth"
    publisher_name = "Mojang"

    empty_session.execute(text('INSERT INTO publishers (name) VALUES (:publisher_name)'),
                          {"publisher_name": publisher_name})

    empty_session.execute(text(
        'INSERT INTO games (game_id, game_title, game_price, release_date, publisher_name) VALUES'
        '(1234, :game_title, 29.99, :date, :publisher_name)'),
        {"game_title": game1_title, "date": release_date, "publisher_name": publisher_name}
    )

    empty_session.execute(text(
        'INSERT INTO games (game_id, game_title, game_price, release_date, publisher_name) VALUES'
        '(2345, :game_title, 59.99, :date, :publisher_name)'),
        {"game_title": game2_title, "date": release_date, "publisher_name": publisher_name}
    )

    game_keys = empty_session.execute(text('SELECT game_id FROM games WHERE publisher_name = :publisher_name'),
                                     {'publisher_name': publisher_name}).mappings().all()

    return [g["game_id"] for g in game_keys]


def insert_genre(empty_session):
    empty_session.execute(text('INSERT INTO genres (genre_name) VALUES ("Action")'))

    genre = empty_session.execute(text('SELECT genre_name FROM genres WHERE genre_name = "Action"')).mappings().one()

    return genre["genre_name"]


def make_genre():
    return Genre("Action")


def insert_game_genre_association(empty_session):
    game_keys = insert_game_publisher_association(empty_session)
    genre = insert_genre(empty_session)

    for game_key in game_keys:
        empty_session.execute(text('INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'),
                                   {"game_id": game_key, "genre_name": genre})

    game_genre_table = empty_session.execute(text('SELECT game_id, genre_name FROM game_genres')).mappings().all()

    return [(g["game_id"], g["genre_name"]) for g in game_genre_table]


def insert_review(empty_session):
    user_key = insert_user(empty_session)[0]
    game_key = insert_game(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        text('INSERT INTO reviews (user_id, game_id, comment, rating, timestamp) VALUES '
        '(:user_id, :game_id, "Comment 1", 4, :timestamp_1),'
        '(:user_id, :game_id, "Comment 2", 2, :timestamp_2)'),
        {'user_id': user_key, 'game_id': game_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute(text('SELECT game_id from games')).fetchone()
    return row[0]


def insert_user_game_into_wishlist(empty_session, user_id, game_id):
    empty_session.execute(
        text('INSERT INTO user_wishlist (user_id, game_id) VALUES (:user_id, :game_id)'),
        {'user_id': user_id, 'game_id': game_id}
    )

def insert_user_game_into_favorite_games(empty_session, user_id, game_id):
    empty_session.execute(
        text('INSERT INTO user_favorite_games (user_id, game_id) VALUES (:user_id, :game_id)'),
        {'user_id': user_id, 'game_id': game_id}
    )


def test_loading_of_users(empty_session):
    users = list()
    users.append(("AndrewT", "1Testing2"))
    users.append(("CindyM", "2Testing3"))
    insert_users(empty_session, users)

    expected = [
        User("AndrewT", "1Testing2"),
        User("CindyM", "2Testing3")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = empty_session.execute(text('SELECT username, password FROM users')).all()
    assert rows == [("YearningShout", "123Testing")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("AnnoyingShout", "Testing123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("AnnoyingShout", "Testing123")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_publishers(empty_session):
    publisher = insert_publisher(empty_session)

    expected_publisher = make_publisher()
    fetched_publisher = empty_session.query(Publisher).one()

    assert expected_publisher == fetched_publisher
    assert publisher == fetched_publisher.publisher_name


def test_loading_of_games(empty_session):
    game_key = insert_game(empty_session)

    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id


def test_game_publisher_association(empty_session):
    game_keys = insert_game_publisher_association(empty_session)

    fetched_games = empty_session.query(Game).all()

    assert len(game_keys) == len(fetched_games)

    for i in range(len(game_keys)):
        assert game_keys[i] == fetched_games[i].game_id


def test_loading_of_genres(empty_session):
    genre = insert_genre(empty_session)

    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert genre == fetched_genre.genre_name


def test_game_genre_association(empty_session):
    games_genre_ids = insert_game_genre_association(empty_session)

    expected_games = empty_session.query(Game).all()
    expected_genres = empty_session.query(Genre).all()

    assert len(expected_genres) == 1

    for i in range(len(games_genre_ids)):
        assert empty_session.query(Game).get(games_genre_ids[i][0]) == expected_games[i]
        assert games_genre_ids[i][1] == expected_genres[0].genre_name


def test_loading_of_game_reviews(empty_session):
    insert_review(empty_session)

    rows = empty_session.query(Review).all()
    review = rows[0]

    assert review.comment == "Comment 1"


def test_saving_of_game_reviews(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("ChickenLittle", "Testing1234"))[0]

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "ChickenLittle").one()

    review_comment = "Some comment text."
    rating = 2
    review = add_review(review_comment, rating, game, user)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_id, game_id, comment, rating FROM reviews')))

    assert rows == [(user_key, game_key, review_comment, rating)]


def test_saving_of_game_to_wishlist(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("Steve", "Testing1234"))[0]

    insert_user_game_into_wishlist(empty_session, user_key, game_key)

    rows = list(empty_session.execute(text('SELECT user_id, game_id FROM user_wishlist')))

    assert rows == [(user_key, game_key)]
    assert empty_session.query(User).get(rows[0][0]) == empty_session.query(User).filter(User._User__username == "Steve").one()
    assert empty_session.query(Game).get(rows[0][1]) == empty_session.query(Game).filter(Game._Game__game_title == "Minecraft").one()


def test_saving_of_game_to_favourite_games(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("Herobrine", "OMGI<3Minecraft"))[0]

    insert_user_game_into_favorite_games(empty_session, user_key, game_key)

    rows = list(empty_session.execute(text('SELECT user_id, game_id FROM user_favorite_games')))

    assert rows == [(user_key, game_key)]
    assert empty_session.query(User).get(rows[0][0]) == empty_session.query(User).filter(User._User__username == "Herobrine").one()
    assert empty_session.query(Game).get(rows[0][1]) == empty_session.query(Game).filter(Game._Game__game_title == "Minecraft").one()
