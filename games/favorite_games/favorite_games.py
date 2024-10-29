# favorite_games_routes.py

from flask import Blueprint, redirect, url_for, render_template
from games.auth.authentication import login_required
from games.auth.services import get_user
from games.domainmodel.model import Game
from games.game_description import services as game_services
import games.adapters.repository as repo
import games.utilities.utilities as u
from games.favorite_games import services

favorite_games_blueprint = Blueprint('favorite_games_bp', __name__)

@favorite_games_blueprint.route('/add_to_favorite/<int:game_id>', methods=['POST'])
@login_required
def add_to_favorite_route(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    if game:
        current_user_name = u.get_current_user()
        currentuser = services.get_user(repo.repo_instance, current_user_name)
        services.add_to_user_favorite(repo.repo_instance,currentuser, game)
    return redirect(url_for('game_description_bp.game_description', game_id=game_id, game_title=game.title))

@favorite_games_blueprint.route('/remove_from_favorite/<int:game_id>', methods=['POST'])
@login_required
def remove_from_favorite_route(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    if game:
        current_user_name = u.get_current_user()
        currentuser = services.get_user(repo.repo_instance, current_user_name)
        services.remove_to_user_favorite(repo.repo_instance,currentuser, game)
    return redirect(url_for('game_description_bp.game_description', game_id=game_id, game_title=game.title))

