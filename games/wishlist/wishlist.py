# wishlist_routes.py

from flask import Blueprint, redirect, render_template, url_for, session, request
from games.auth.authentication import login_required
from games.auth.services import get_user
from games.domainmodel.model import Game
from games.game_description import services as game_services
#from .services import add_to_wishlist, remove_from_wishlist, get_wishlist
#from games.adapters.memory_repository import add
import games.adapters.repository as repo
import games.utilities.utilities as u
from games.wishlist import services

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
@login_required
def add_to_wishlist_route(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    if game:
        current_user_name = u.get_current_user()
        currentuser = services.get_user(repo.repo_instance, current_user_name)
        services.add_to_user_wishlist(repo.repo_instance, currentuser, game)
    return redirect(url_for('game_description_bp.game_description', game_id=game_id, game_title=game.title))

@wishlist_blueprint.route('/remove_from_wishlist/<int:game_id>', methods=['POST'])
@login_required
def remove_from_wishlist_route(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    if game:
        current_user_name = u.get_current_user()
        currentuser = services.get_user(repo.repo_instance, current_user_name)
        services.remove_from_user_wishlist(repo.repo_instance, currentuser, game)
    return redirect(url_for('game_description_bp.game_description', game_id=game_id, game_title=game.title))

@wishlist_blueprint.route('/wishlist', methods=['GET'])
@login_required
def user_wishlist_route():
    current_user_name = u.get_current_user()
    currentuser = services.get_user(repo.repo_instance, current_user_name)
    wishlist = services.get_wishlist(repo.repo_instance,currentuser)
    return render_template('wishlist.html', wishlist=wishlist, current_user = u.get_current_user())
