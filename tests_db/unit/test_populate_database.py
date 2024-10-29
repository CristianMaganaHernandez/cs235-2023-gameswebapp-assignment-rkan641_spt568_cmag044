from sqlalchemy import select, inspect

from games.adapters.orm import metadata

# Using data from ../tests/data/games.csv


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == [
        'game_genres',
        'games',
        'genres',
        'publishers',
        'reviews',
        'user_favorite_games',
        'user_wishlist',
        'users',
    ]


def test_database_populate_select_all_games(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(metadata.tables[name_of_games_table])
        result = connection.execute(select_statement).mappings().all()

        all_games = []

        # Didn't append other 4 rows
        for row in result:
            all_games.append((
                row['game_id'],
                row['game_title'],
                row['game_price'],
                row['release_date']
            ))

        assert len(all_games) == 8
        assert all_games[0] == (
            7940,
            "Call of Duty® 4: Modern Warfare®",
            9.99,
            "Nov 12, 2007"
        )


def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select(metadata.tables[name_of_genres_table])
        result = connection.execute(select_statement).mappings().all()

        all_genres = []
        for row in result:
            all_genres.append(row["genre_name"])

        assert len(all_genres) == 1

        assert all_genres[0] == 'Action'


def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table publishers
        select_statement = select(metadata.tables[name_of_publishers_table])
        result = connection.execute(select_statement).mappings().all()

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])

        assert len(all_publishers) == 8

        select_publishers = [
            'KOEI TECMO GAMES CO., LTD.',
            'I-Illusions',
            'Buka Entertainment',
            'D3PUBLISHER',
            'Komodo',
            'Beep Games, Inc.'
        ]

        for p in select_publishers:
            assert p in all_publishers
