import random
from flask import Blueprint, render_template
import games.adapters.repository as repo
import games.utilities.utilities as u

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    games = repo.repo_instance.get_games()

    if games:
        a_game = random.choice(games)
    else:
        a_game = None

    return render_template('home.html',
                           game=a_game,
                           current_user=u.get_current_user())

