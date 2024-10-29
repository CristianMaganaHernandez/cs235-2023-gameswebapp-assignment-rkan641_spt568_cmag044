import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables

from games.domainmodel.model import User, Game
import datetime

from pathlib import Path

project_root = Path(__file__).parent.parent

TEST_DATA_PATH_DATABASE_FULL = project_root / "games" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = project_root / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///games-test.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    with engine.connect() as e:
        for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
            e.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode)
    yield engine
    metadata.drop_all(engine)


# Engine is different
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    with engine.connect() as e:
        for table in reversed(metadata.sorted_tables):
            e.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_FULL, repo_instance, database_mode)

    # Insert user and game into session
    user = User("Cris", "TheBuilder<3")
    game = Game(5121, "CSGO")
    game.price = 2.99
    game.release_date = datetime.date(2011, 11, 18).strftime("%b %d, %Y")

    repo_instance.add_user(user)
    repo_instance.add_game(game)

    yield session_factory
    metadata.drop_all(engine)


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    with engine.connect() as e:
        for table in reversed(metadata.sorted_tables):
            e.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)