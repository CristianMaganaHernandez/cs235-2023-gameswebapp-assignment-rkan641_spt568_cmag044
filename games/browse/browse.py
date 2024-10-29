from flask import Blueprint, render_template, request
from games.browse import services
import games.adapters.repository as repo
import games.utilities.utilities as u
from games.browse import services


browse_blueprint = Blueprint('games_bp', __name__)


@browse_blueprint.route('/browse/<browse_genre>', methods=['GET', 'POST'])
@browse_blueprint.route('/browse/<browse_genre>/<int:page>', methods=['GET', 'POST'])
def browse_games(page=1, browse_genre="All"):
    page_size = 10

    # Redo replacement from genre_sidebar.html so page can actually load
    browse_genre = browse_genre.replace("_", " ")

    num_games = services.get_number_of_games_by_genre(repo.repo_instance, browse_genre)
    total_pages = (num_games + page_size - 1) // page_size

    # The 'Go to Page' functionality
    if request.method == "POST":
        requested_page = request.form['goto_query']
        try:
            requested_page = int(requested_page)
            if total_pages >= requested_page >= 1:
                page = requested_page
        except ValueError:
            pass
            # currently does not need any exception since it just needs to block incorrect inputs

            # flashing messages does not work. The secret key in .env is not being recognised
            # flash("Please enter a valid number")


    # Calculate the offset for pagination
    offset = (page - 1) * page_size

    # Fetch games for the current page
    current_page_games = services.get_games_pagination(repo.repo_instance, genre=browse_genre, offset=offset, limit=page_size, order_by='game_title')


    # Fetch all genres for the genre sidebar
    game_genres = services.get_game_genres(repo.repo_instance)

    return render_template(
        'browse.html',
        games=current_page_games,
        num_games=num_games,
        prev_page=page - 1 if page > 1 else None,
        next_page=page + 1 if page < total_pages else None,
        current_page=page,
        total_pages=total_pages,
        genres=game_genres,
        current_genre=browse_genre,
        current_user=u.get_current_user()
    )
