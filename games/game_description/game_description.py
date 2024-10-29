
from flask import Blueprint, render_template, flash, redirect, url_for, request, session

from games.auth.authentication import login_required
from games.auth.services import get_user
from games.domainmodel.model import Review
from games.game_description import services
import games.adapters.repository as repo

import games.utilities.utilities as u


game_description_blueprint = Blueprint('game_description_bp', __name__)


# Although game_title is unused in function, it is used in the URL
@game_description_blueprint.route('/<game_title>/<int:game_id>', methods=['GET'])
def game_description(game_id, game_title):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    if not game:
        return "Game not found", 404

    average_rating = services.calculate_average_rating(repo.repo_instance, game.game_id, game.reviews)
    if average_rating is None:
        average_rating = 0  # or another default value
    else:
        average_rating = round(average_rating, 1)

    average_rating = round(average_rating, 1)
    return render_template('game_description.html', game=game,average_rating=average_rating, current_user = u.get_current_user())


@game_description_blueprint.route('/submit_review/<int:game_id>/<game_title>', methods=['POST'])
@login_required
def submit_review(game_id, game_title, rating=None, comment=None):

    if 'user_name' not in session:
        return redirect(url_for('auth_bp.user_login'))

    current_user_name = u.get_current_user()

    currentuser = services.get_user(repo.repo_instance,current_user_name)

    game = services.get_game_by_id(repo.repo_instance, game_id)

    if not game:
        return "Game not found", 404

    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')

    services.add_review(repo.repo_instance, comment, rating, game, currentuser)
    game.reviews.sort(key=lambda r: r._Review__timestamp, reverse=True)

    return redirect(url_for('game_description_bp.game_description', game_id=game_id, game_title=game_title))
