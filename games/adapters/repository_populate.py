from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):

    games_file_name = str(Path(data_path) / "games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    publishers = list(reader.dataset_of_publishers)
    genres = list(reader.dataset_of_genres)
    games = reader.dataset_of_games

    # Add publishers to the repo
    repo.add_multiple_publishers(publishers)

    # Add genres to the repo
    repo.add_multiple_genres(genres)

    # Add games to the repo
    repo.add_multiple_games(games)
