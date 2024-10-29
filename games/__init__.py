from flask import Flask
from pathlib import Path
import config

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables
from games.adapters.memory_repository import populate2


def create_app(test_config=None):
    """Construct the core application."""
    app = Flask(__name__)

    # Add env variables from the config
    app.config.from_object(config.Config)
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        data_path = Path('games') / 'adapters' / 'data'
        # populate(data_path, repo.repo_instance, database_mode)
        populate2(repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':

        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

        # Setup database with SQLAlchemy
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)
            with database_engine.connect() as conn:
                for table in reversed(metadata.sorted_tables):
                    conn.execute(table.delete())
            map_model_to_tables()
            database_mode = True
            populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_model_to_tables()

    # Blueprint registration
    with app.app_context():
        from .browse.browse import browse_blueprint
        app.register_blueprint(browse_blueprint)

        from .home.home import home_blueprint
        app.register_blueprint(home_blueprint)

        from .search.search import search_blueprint
        app.register_blueprint(search_blueprint)

        from .game_description.game_description import game_description_blueprint
        app.register_blueprint(game_description_blueprint)

        from .profile.profile import profile_blueprint
        app.register_blueprint(profile_blueprint)

        # Auth
        from .auth.authentication import authentication_blueprint
        app.register_blueprint(authentication_blueprint)

        from .wishlist.wishlist import wishlist_blueprint
        app.register_blueprint(wishlist_blueprint)

        from .favorite_games.favorite_games import favorite_games_blueprint
        app.register_blueprint(favorite_games_blueprint)

    return app
