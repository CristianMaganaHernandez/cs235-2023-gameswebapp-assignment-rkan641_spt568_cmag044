from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey, DateTime
)
from sqlalchemy.orm import registry, mapper, relationship
from games.domainmodel.model import Game, User, Genre, Review, Publisher

mapper_registry = registry()

metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')))

genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)


users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(20), unique=True, nullable=False),
    Column('password', String(20), nullable=False)
)

user_wishlist_table = Table(
    'user_wishlist', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('game_id', ForeignKey('games.game_id'), primary_key=True)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('timestamp', DateTime, nullable=True),
    Column('comment', String(255), nullable=True),
    Column('rating', Integer, nullable=False),
    Column('user_id', ForeignKey('users.user_id')),
    Column('game_id', ForeignKey('games.game_id'))
)


user_favorite_games_table = Table(
    'user_favorite_games', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('game_id', ForeignKey('games.game_id'), primary_key=True)
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper_registry.map_imperatively(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__publisher': relationship(Publisher, backref='games'),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
        '_Game__genres': relationship(Genre, secondary=game_genres_table)
    })

    mapper_registry.map_imperatively(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__favourite_games': relationship(Game, secondary=user_favorite_games_table, backref='_Game__favorited_by_users'),
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__wishlist': relationship(Game, secondary=user_wishlist_table, backref='_Game__wishlisted_by_users')
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_Review__review_id': reviews_table.c.review_id,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })