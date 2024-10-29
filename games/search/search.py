from flask import Blueprint, render_template, request
from games.search import services
import games.adapters.repository as repo
import games.utilities.utilities as u

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search_games():
    if request.method == 'POST':
        search_query = request.form['search_query']
        selected_filter = request.form['filter']
        price_filter = request.form.getlist('price_filter')

        search_results = services.search_games(repo.repo_instance,search_query, selected_filter, price_filter)
    else:
        search_query = None
        search_results = []

    return render_template('search.html',
                           search_query=search_query,
                           search_results=search_results,
                           current_user=u.get_current_user()
                           )